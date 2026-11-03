"""Freeze all completed responses, then extract and score the named Game fields."""
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TRUTH={'sample_01':'Breakout','sample_02':'Pong','sample_03':'Pac-Man','sample_04':'Freeway'}
PATTERNS={'Breakout':r'\bbreakout\b|\barkanoid\b','Pong':r'\bpong\b',
          'Pac-Man':r'\bpac[\s\-]?man\b','Freeway':r'\bfreeway\b|\bfrogger\b'}


def extract(text):
    clean=text.replace('**','').replace('__','')
    clean=re.sub(r'(?m)^#{1,6}\s*','',clean)
    game=re.search(r'^Game:\s*(.*?)(?=\n\s*Description:|\Z)',clean,re.M|re.S)
    confidence=re.search(r'^Confidence:\s*(\d+(?:\.\d+)?)\s*%',clean,re.M)
    if not game:raise ValueError('Missing Game field; preserve response and review manually.')
    return game.group(1).strip(),float(confidence.group(1)) if confidence else None


def main():
    folders=sorted((ROOT/'runs').iterdir())
    runs=[json.loads((p/'run.json').read_text()) for p in folders]
    aliases=list(dict.fromkeys(r['alias'] for r in runs))
    assert all(sum(r['alias']==a for r in runs)==5 for a in aliases),'Wait for all five cases per model.'
    assert all(r['status']=='completed' and r['exit_code']==0 and r['tool_free'] for r in runs)
    answers={str(p.relative_to(ROOT))+'/answer.md':hashlib.sha256((p/'answer.md').read_bytes()).hexdigest() for p in folders}
    (ROOT/'operator/answers-frozen.json').write_text(json.dumps({'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':answers},indent=2))
    results=[]
    for folder,run in zip(folders,runs):
        answer=(folder/'answer.md').read_text();guess,confidence=extract(answer)
        expected_hash=hashlib.sha256((ROOT/'prompts'/f"{run['sample']}.txt").read_bytes()).hexdigest()
        assert run['prompt_sha256']==expected_hash
        matches=[label for label,pattern in PATTERNS.items() if re.search(pattern,guess,re.I)]
        actual=TRUTH.get(run['sample']);correct=(actual in matches) if actual else None
        row={'model':run['requested_model'],'alias':run['alias'],'sample':run['sample'],'actual_game':actual,
             'guess':guess,'confidence_percent':confidence,'matched_game_keywords':matches,
             'correct_by_keyword_rule':correct,'needs_manual_review':bool(actual and len(matches)>1),
             'tool_free':run['tool_free'],'requested_effort':run['requested_effort'],
             'model_verification':'response/init IDs' if run['provider']=='claude' else 'exact pinned CLI request; response ID not exposed in JSON stream',
             'seconds':run['seconds'],'prompt_sha256':run['prompt_sha256'],
             'answer_sha256':run['answer_sha256'],'final_explanation':answer,
             'usage':run.get('result',{}).get('usage',{}) if run['provider']=='claude' else run.get('turns',[]),
             'cli_reported_cost_usd':run.get('result',{}).get('total_cost_usd')}
        results.append(row)
    summary=[]
    for alias in aliases:
        primary=[x for x in results if x['alias']==alias and x['actual_game']]
        control=next(x for x in results if x['alias']==alias and not x['actual_game'])
        summary.append({'alias':alias,'correct':sum(x['correct_by_keyword_rule'] for x in primary),'total':4,
                        'shape_control':control['guess'],'shape_confidence_percent':control['confidence_percent'],
                        'primary':[{k:x[k] for k in ['actual_game','guess','confidence_percent','correct_by_keyword_rule']} for x in primary]})
    report={'source_credit':'Takehi, Teoh, Zhang and Khattab (2026), CC BY 4.0 experiment data',
            'source_repo':'https://github.com/RikiyaT/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game',
            'effort':'high for every run; effort labels do not imply equal computation across models',
            'scoring':'Original Game-field keyword rule; Frogger accepted for Freeway. Ambiguous multi-game fields flagged for manual review.',
            'notes':['Each primary prompt is byte-identical to the released source, including 17,253 numerical actor weights rounded to three decimals.',
                     'One fresh response per checkpoint, no tools or game candidate list. No retries based on answers.',
                     'One common shape/layout-only diagnostic per model, not four independent controls.',
                     'Game guesses scored; numerical explanations not exhaustively verified. One selected training checkpoint per game.'],
            'summary':summary,'cases':results}
    (ROOT/'operator/results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
