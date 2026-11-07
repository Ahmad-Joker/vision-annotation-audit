import argparse
import json
import sys
from pathlib import Path
from .core import audit


def markdown(report):
    s=report['summary']
    lines=['# Vision Annotation Audit','',f"Images: {s['images']} | Annotations: {s['annotations']} | Categories: {s['categories']}",f"Errors: {s['errors']} | Warnings: {s['warnings']}",'','| Severity | Code | Location | Description |','|---|---|---|---|']
    for i in report['issues']:
        lines.append('| '+' | '.join(str(i[k]).replace('|','\\|').replace('\n',' ') for k in ('severity','code','location','message'))+' |')
    if not report['issues']: lines.append('| OK | - | - | No issues detected |')
    return '\n'.join(lines)+'\n'


def main(argv=None):
    p=argparse.ArgumentParser(description='Audit COCO JSON annotation quality')
    p.add_argument('input',help='COCO JSON file')
    p.add_argument('--json-out',help='Write machine-readable report')
    p.add_argument('--md-out',help='Write Markdown report')
    p.add_argument('--area-tolerance',type=float,default=0.15)
    a=p.parse_args(argv)
    if not 0<=a.area_tolerance<=1:
        p.error('--area-tolerance must be in [0,1]')
    try:
        data=json.loads(Path(a.input).read_text(encoding='utf-8'))
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        print(f'Input error: {exc}',file=sys.stderr)
        return 3
    report=audit(data,area_tolerance=a.area_tolerance)
    try:
        if a.json_out: Path(a.json_out).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        if a.md_out: Path(a.md_out).write_text(markdown(report),encoding='utf-8')
    except OSError as exc:
        print(f'Output error: {exc}',file=sys.stderr)
        return 3
    print(json.dumps(report['summary'],sort_keys=True))
    return 2 if report['summary']['errors'] else 0

if __name__=='__main__':
    sys.exit(main())
