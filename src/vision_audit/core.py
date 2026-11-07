"""Deterministic, stdlib-only COCO JSON quality checks."""
from collections import Counter, defaultdict
from math import isfinite


def audit(data, *, area_tolerance=0.15):
    issues = []
    def issue(code, severity, location, message):
        issues.append(dict(code=code, severity=severity, location=location, message=message))
    if not isinstance(data, dict):
        issue('ROOT_TYPE', 'error', '$', 'COCO root must be an object')
        return {'summary': {'images': 0, 'annotations': 0, 'categories': 0, 'errors': 1, 'warnings': 0}, 'issues': issues}
    maps = {}
    for key in ('images', 'annotations', 'categories'):
        records = data.get(key)
        if not isinstance(records, list):
            issue('MISSING_LIST', 'error', key, f'{key} must be a list')
            records = []
        maps[key] = records
    ids = {}
    for key, records in maps.items():
        found = set()
        for i, obj in enumerate(records):
            loc = f'{key}[{i}]'
            if not isinstance(obj, dict):
                issue('RECORD_TYPE', 'error', loc, 'Record must be an object')
                continue
            ident = obj.get('id')
            if not isinstance(ident, int) or isinstance(ident, bool):
                issue('INVALID_ID', 'error', loc, 'id must be an integer')
            elif ident in found:
                issue('DUPLICATE_ID', 'error', loc, f'Duplicate id {ident}')
            else:
                found.add(ident)
        ids[key] = found
    images = {}
    for i, img in enumerate(maps['images']):
        if not isinstance(img, dict): continue
        w, h = img.get('width'), img.get('height')
        if not all(isinstance(x, (int,float)) and not isinstance(x,bool) and isfinite(x) and x>0 for x in (w,h)):
            issue('IMAGE_DIMENSIONS', 'error', f'images[{i}]', 'Image dimensions must be positive finite numbers')
        if isinstance(img.get('id'), int) and not isinstance(img.get('id'), bool) and img.get('id') in ids['images'] and img.get('id') not in images:
            images[img['id']] = img
    counts = Counter()
    boxes = defaultdict(list)
    for i, ann in enumerate(maps['annotations']):
        if not isinstance(ann, dict): continue
        loc=f'annotations[{i}]'
        imid, catid = ann.get('image_id'), ann.get('category_id')
        if not isinstance(imid, int) or isinstance(imid, bool) or imid not in ids['images']: issue('UNKNOWN_IMAGE', 'error', loc, f'Unknown image_id {imid}')
        if not isinstance(catid, int) or isinstance(catid, bool) or catid not in ids['categories']: issue('UNKNOWN_CATEGORY', 'error', loc, f'Unknown category_id {catid}')
        else: counts[catid]+=1
        bbox=ann.get('bbox')
        if not isinstance(bbox,list) or len(bbox)!=4 or not all(isinstance(x,(int,float)) and not isinstance(x,bool) and isfinite(x) for x in bbox):
            issue('INVALID_BBOX', 'error', loc, 'bbox must be four finite numbers')
            continue
        x,y,w,h=bbox
        if w<=0 or h<=0: issue('NONPOSITIVE_BBOX', 'error', loc, 'bbox width and height must be positive')
        if x<0 or y<0: issue('NEGATIVE_ORIGIN', 'error', loc, 'bbox origin cannot be negative')
        im=images.get(imid)
        if im and all(isinstance(im.get(k),(int,float)) and isfinite(im[k]) and im[k]>0 for k in ('width','height')) and (x+w>im['width']+1e-8 or y+h>im['height']+1e-8):
            issue('OUT_OF_BOUNDS', 'error', loc, 'bbox extends outside image')
        area=ann.get('area')
        if area is not None:
            if not isinstance(area,(int,float)) or isinstance(area,bool) or not isfinite(area) or area<0:
                issue('INVALID_AREA', 'error', loc, 'area must be finite and nonnegative')
            elif w>0 and h>0 and abs(area-w*h)/max(w*h,1e-12)>area_tolerance:
                issue('AREA_MISMATCH', 'warning', loc, 'area differs from bbox area (may be valid for segmentation)')
        if w>0 and h>0:
            key=(imid,catid,tuple(round(v,5) for v in bbox))
            if key in boxes: issue('DUPLICATE_BOX', 'warning', loc, f'Same image/category/bbox as annotations[{boxes[key][0]}]')
            boxes[key].append(i)
    for i, cat in enumerate(maps['categories']):
        if isinstance(cat,dict) and isinstance(cat.get('id'),int) and not isinstance(cat.get('id'),bool) and cat.get('id') in ids['categories'] and counts[cat['id']]==0:
            issue('EMPTY_CATEGORY','warning',f'categories[{i}]','No annotations for this category')
    issues.sort(key=lambda v:(v['location'],v['code'],v['message']))
    return {'summary': {'images':len(maps['images']), 'annotations':len(maps['annotations']), 'categories':len(maps['categories']), 'errors':sum(i['severity']=='error' for i in issues), 'warnings':sum(i['severity']=='warning' for i in issues)}, 'issues':issues}
