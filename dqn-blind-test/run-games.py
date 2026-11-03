"""Run fresh Codex CLI processes with only the fixed tensor MCP surface."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PYTHON=Path(sys.executable).absolute()
DISABLED=['shell_tool','unified_exec','unified_exec_tty','shell_snapshot','view_image','image_generation','multi_agent','multi_agent_v2','apps','plugins','remote_plugin','browser_use','browser_use_external','browser_use_full_cdp_access','in_app_browser','computer_use','code_mode','skill_search','skill_mcp_dependency_install','sleep_tool','tool_suggest','goals','hooks','workspace_dependencies','memories','daemon_auto_start']
BASE_PROMPT='You are examining one anonymous neural-network checkpoint from a game-playing agent. Predict the specific game it was trained to play, using only the supplied tensor reader. No candidate game list is supplied.\n\nOriginal filenames, paths, tensor names, metadata, code, training logs, game images, videos, examples, and project context are withheld. IDs do not describe connectivity. Shapes and dtypes are retained. You may inspect numerical tensors through the available reader, but may not run the network or its layers on any input, obtain activations, train, access files or the internet, or execute host code.\n\nGive your best concrete game-name guess even if confidence is low, and clearly label speculation. Distinguish evidence from architecture/output dimensions from evidence in learned numerical values. Recognizing a common game-agent architecture or action count alone is not evidence of learned game-specific features. Report architecture confidence and exact-game confidence separately. In task_hypotheses, provide 3-5 ranked game-name hypotheses with probabilities summing to 1, including unknown/other when warranted. Use best_task_guess for your best specific game guess.\n\nUse at most 24 reader calls, then return the final JSON answer. Do not ask for candidate games or hints.\n'
SCHEMA={"type":"object","additionalProperties":False,"properties":{
"architecture":{"type":"string"},"architecture_confidence":{"type":"number","minimum":0,"maximum":1},
"input_modality":{"type":"string"},"output_structure":{"type":"string"},
"best_task_guess":{"type":"string"},"task_confidence":{"type":"number","minimum":0,"maximum":1},
"task_hypotheses":{"type":"array","minItems":3,"maxItems":5,"items":{"type":"object","additionalProperties":False,"properties":{"task":{"type":"string"},"probability":{"type":"number","minimum":0,"maximum":1},"evidence":{"type":"string"}},"required":["task","probability","evidence"]}},
"numerical_evidence":{"type":"array","items":{"type":"string"}},
"shape_evidence":{"type":"array","items":{"type":"string"}},
"limitations":{"type":"array","items":{"type":"string"}}
},"required":["architecture","architecture_confidence","input_modality","output_structure","best_task_guess","task_confidence","task_hypotheses","numerical_evidence","shape_evidence","limitations"]}


def flags(folder, sample, shapes_only):
    args=['-m','gpt-6-astra','-s','read-only','-c','model_reasoning_effort="xhigh"','-c','approval_policy="never"','-c','web_search="disabled"','-c','project_doc_max_bytes=0','-c',f'model_instructions_file={json.dumps(str(ROOT/"instructions.md"))}','-c','skills.include_instructions=false','-c','skills.bundled.enabled=false','-c','features.skip_host_skill_discovery=true','-c','features.code_mode_host=true']
    for feature in DISABLED: args+=['--disable',feature]
    reader_args=[str(ROOT/'reader.py'),'--payload',str(ROOT/'payloads'/f'{sample}.npz'),'--audit',str(folder/'reader.jsonl')]
    if shapes_only: reader_args+=['--shapes-only']
    args+=['-c',f'mcp_servers.tensors.command={json.dumps(str(PYTHON))}','-c',f'mcp_servers.tensors.args={json.dumps(reader_args)}','-c','mcp_servers.tensors.startup_timeout_sec=30','-c','mcp_servers.tensors.tool_timeout_sec=60','-c','mcp_servers.tensors.default_tools_approval_mode="auto"']
    return args


def run_one(sample,condition):
    folder=ROOT/'runs'/f'{sample}_{condition}'
    folder.mkdir(parents=True,exist_ok=False)
    workspace=folder/'workspace';workspace.mkdir()
    shapes_only=condition=='shapes'
    prompt=BASE_PROMPT+ ('\nCondition: only tensor IDs, shapes, dtypes, and entry counts are available. No numerical values or value-derived statistics are provided.\n' if shapes_only else '\nCondition: all numerical values of the anonymous tensors are available through the tools, as well as shapes and dtypes.\n')
    (folder/'prompt.txt').write_text(prompt)
    cmd=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check','--json','--color','never','--output-schema',str(ROOT/'schema.json'),'-o',str(folder/'answer.json'),'-C',str(workspace),*flags(folder,sample,shapes_only),'-']
    # No parent transcript, task name, repo path, or original filename is passed.
    clean_env={k:v for k,v in os.environ.items() if not (k.startswith('CODEX_') or k.startswith('CLAUDE_') or k in {'PWD','OLDPWD','INIT_CWD'})}
    clean_env['PWD']=str(workspace)
    started=time.time()
    record=dict(sample=sample,condition=condition,model='gpt-6-astra',reasoning_effort='xhigh',command=cmd,started=datetime.datetime.now(datetime.timezone.utc).isoformat(),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),status='running')
    (folder/'run.json').write_text(json.dumps(record,indent=2))
    print('START',sample,condition,flush=True)
    with (folder/'events.jsonl').open('w') as out,(folder/'stderr.txt').open('w') as err:
        try:
            proc=subprocess.run(cmd,input=prompt,text=True,cwd=workspace,env=clean_env,stdout=out,stderr=err,timeout=900)
            record['exit_code']=proc.returncode
            record['status']='completed' if proc.returncode==0 and (folder/'answer.json').exists() else 'failed'
        except subprocess.TimeoutExpired:
            record['status']='timed_out'
    record['seconds']=time.time()-started
    events=[]
    for line in (folder/'events.jsonl').read_text().splitlines():
        try: events.append(json.loads(line))
        except json.JSONDecodeError: pass
    items=[e.get('item',{}) for e in events if e.get('type')=='item.completed']
    tool_items=[i for i in items if i.get('type') not in {'agent_message','reasoning','error'}]
    unexpected=[i for i in tool_items if i.get('type')!='mcp_tool_call' or i.get('server')!='tensors']
    reader_calls=[]
    if (folder/'reader.jsonl').exists():
        reader_calls=[json.loads(line) for line in (folder/'reader.jsonl').read_text().splitlines()]
    record['audit']=dict(completed_item_types=sorted(set(i.get('type','') for i in items)),unexpected_tool_items=unexpected,reader_calls=len(reader_calls),reader_operations=sorted(set(r['request']['name'] for r in reader_calls)),tool_surface_passed=not unexpected)
    completed=[e for e in events if e.get('type')=='turn.completed']
    record['turns']=completed
    (folder/'run.json').write_text(json.dumps(record,indent=2))
    print('END',sample,condition,record['status'],round(record['seconds'],1),'seconds','calls',len(reader_calls),flush=True)
    return record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--only',nargs=2,metavar=('SAMPLE','CONDITION'))
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--remaining',action='store_true',help='Run only cases without an existing run folder.')
    args=parser.parse_args()
    (ROOT/'instructions.md').write_text('You are a careful scientific analyst. Follow the user request using only supplied data and tools. Distinguish observations from conjectures.\n')
    (ROOT/'schema.json').write_text(json.dumps(SCHEMA,indent=2))
    cases=[tuple(args.only)] if args.only else [('sample_01','shapes'),('sample_02','shapes'),('sample_03','shapes'),('sample_01','weights'),('sample_02','weights'),('sample_03','weights')]
    if args.remaining:
        cases=[case for case in cases if not (ROOT/'runs'/f'{case[0]}_{case[1]}').exists()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records=list(pool.map(lambda case:run_one(*case),cases))
    print(json.dumps([dict(sample=r['sample'],condition=r['condition'],status=r['status']) for r in records]),flush=True)


if __name__=='__main__':main()
