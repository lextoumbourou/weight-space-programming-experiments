"""Tool-free cross-model replay of the authors' unchanged Experiment 1 prompts."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MODELS={'sol':('codex','gpt-6.1-sol'),'terra':('codex','gpt-6.1-terra'),
        'opus':('claude','claude-opus-5-5'),'sonnet':('claude','claude-sonnet-5-5'),'haiku':('claude','claude-haiku-5-5')}
EFFORT='high'
DISABLED=['shell_tool','unified_exec','unified_exec_tty','shell_snapshot','view_image',
          'image_generation','multi_agent','multi_agent_v2','apps','plugins','remote_plugin',
          'browser_use','browser_use_external','browser_use_full_cdp_access','in_app_browser',
          'computer_use','code_mode','code_mode_host','skill_search','skill_mcp_dependency_install',
          'sleep_tool','tool_suggest','goals','hooks','worktrees','workspace_dependencies',
          'memories','daemon_auto_start','collaboration_modes']


def run_one(case):
    alias,sample=case
    provider,model=MODELS[alias]
    folder=ROOT/'runs'/f'{alias}_{sample}';folder.mkdir(exist_ok=False)
    workspace=folder/'workspace';workspace.mkdir()
    prompt=(ROOT/'prompts'/f'{sample}.txt').read_text()
    if provider=='claude':
        cmd=['claude','-p','--bare','--restricted','--model',model,'--effort',EFFORT,
             '--tools','','--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
             '--disable-slash-commands','--no-session-persistence','--setting-sources','',
             '--settings',json.dumps({'disableAllHooks':True,'autoMemoryEnabled':False,'fastMode':False}),
             '--system-prompt',(ROOT/'instructions.md').read_text(),'--permission-prompts','none',
             '--output-format','stream-json','--verbose','--max-turns','1']
    else:
        cmd=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral',
             '--skip-git-repo-check','--json','--color','never','-o',str(folder/'answer.md'),
             '-C',str(workspace),'-m',model,'-s','read-only',
             '-c',f'model_reasoning_effort="{EFFORT}"','-c','model_reasoning_summary="detailed"',
             '-c','approval_policy="never"','-c','web_search="disabled"',
             '-c','project_doc_max_bytes=0','-c',f'model_instructions_file={json.dumps(str(ROOT/"instructions.md"))}',
             '-c','skills.include_instructions=false','-c','skills.bundled.enabled=false',
             '-c','features.skip_host_skill_discovery=true']
        for feature in DISABLED:cmd+=['--disable',feature]
        cmd+=['-']
    env={k:v for k,v in os.environ.items() if not (k.startswith(('CLAUDE_','CODEX_')) or
         k in {'PWD','OLDPWD','INIT_CWD','ANTHROPIC_MODEL','ANTHROPIC_SMALL_FAST_MODEL'} or
         k.startswith('ANTHROPIC_DEFAULT_'))}
    env['PWD']=str(workspace)
    record=dict(alias=alias,sample=sample,provider=provider,requested_model=model,
                requested_effort=EFFORT,command=cmd,
                started=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),status='running')
    (folder/'run.json').write_text(json.dumps(record,indent=2))
    print('START',alias,sample,flush=True);started=time.time()
    with (folder/'events.jsonl').open('w') as out,(folder/'stderr.txt').open('w') as err:
        try:
            proc=subprocess.run(cmd,input=prompt,text=True,cwd=workspace,env=env,
                                stdout=out,stderr=err,timeout=900)
            record['exit_code']=proc.returncode
        except subprocess.TimeoutExpired:record['exit_code']=None
    events=[]
    for line in (folder/'events.jsonl').read_text().splitlines():
        try:events.append(json.loads(line))
        except json.JSONDecodeError:pass
    if provider=='claude':
        inits=[e for e in events if e.get('type')=='system' and e.get('subtype')=='init']
        assistants=[e for e in events if e.get('type')=='assistant']
        tools=[c for e in assistants for c in e.get('message',{}).get('content',[])
               if c.get('type') in {'tool_use','server_tool_use'}]
        results=[e for e in events if e.get('type')=='result'];final=results[-1] if results else {}
        models=sorted({e.get('message',{}).get('model','') for e in assistants})
        record.update(init=inits,tool_calls=tools,observed_models=models,result=final)
        record['tool_free']=not tools and bool(inits) and all(not e.get('tools') and not e.get('mcp_servers') for e in inits)
        success=final.get('subtype')=='success' and models and all(model in m for m in models)
        if 'result' in final:(folder/'answer.md').write_text(final['result']+'\n')
    else:
        items=[e.get('item',{}) for e in events if e.get('type')=='item.completed']
        tools=[i for i in items if i.get('type') not in {'agent_message','reasoning','error'}]
        completed=[e for e in events if e.get('type')=='turn.completed']
        failed=[e for e in events if e.get('type') in {'turn.failed','error'}]
        record.update(tool_calls=tools,completed_item_types=sorted({i.get('type','') for i in items}),
                      turns=completed,failures=failed)
        record['tool_free']=not tools
        record['observed_model_note']='The CLI pins the requested model; its public JSON stream may not expose a response model ID. No fallback is configured.'
        success=bool(completed) and not failed
    record['seconds']=time.time()-started
    answer=folder/'answer.md'
    record['status']='completed' if record['exit_code']==0 and success and record['tool_free'] and answer.exists() and answer.stat().st_size else 'failed'
    if answer.exists():record['answer_sha256']=hashlib.sha256(answer.read_bytes()).hexdigest()
    (folder/'run.json').write_text(json.dumps(record,indent=2))
    print('END',alias,sample,record['status'],round(record['seconds'],1),'tool_free',record['tool_free'],flush=True)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--models',nargs='+',choices=MODELS,default=list(MODELS))
    p.add_argument('--samples',nargs='+',default=['shapes','sample_01','sample_02','sample_03','sample_04'])
    p.add_argument('--workers',type=int,default=4);a=p.parse_args()
    cases=[(m,s) for s in a.samples for m in a.models]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:records=list(pool.map(run_one,cases))
    print(json.dumps([{k:r.get(k) for k in ['alias','sample','status','seconds','tool_free']} for r in records]),flush=True)
