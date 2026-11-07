import json
import unittest
from pathlib import Path
from vision_audit import audit
from vision_audit.__main__ import markdown,main
ROOT=Path(__file__).resolve().parents[1]

class AuditTests(unittest.TestCase):
    def setUp(self): self.clean=json.loads((ROOT/'examples/clean.json').read_text())
    def codes(self,d): return {i['code'] for i in audit(d)['issues']}
    def test_clean(self): self.assertEqual(audit(self.clean)['summary']['errors'],0)
    def test_root(self): self.assertIn('ROOT_TYPE',self.codes([]))
    def test_missing(self): self.assertIn('MISSING_LIST',self.codes({}))
    def test_duplicate_id(self): self.clean['images'].append(self.clean['images'][0]);self.assertIn('DUPLICATE_ID',self.codes(self.clean))
    def test_bad_image(self): self.clean['images'][0]['width']=0;self.assertIn('IMAGE_DIMENSIONS',self.codes(self.clean))
    def test_unknown_image(self): self.clean['annotations'][0]['image_id']=8;self.assertIn('UNKNOWN_IMAGE',self.codes(self.clean))
    def test_unknown_category(self): self.clean['annotations'][0]['category_id']=8;self.assertIn('UNKNOWN_CATEGORY',self.codes(self.clean))
    def test_bad_bbox(self): self.clean['annotations'][0]['bbox']=[1,2,3];self.assertIn('INVALID_BBOX',self.codes(self.clean))
    def test_negative_width(self): self.clean['annotations'][0]['bbox'][2]=-3;self.assertIn('NONPOSITIVE_BBOX',self.codes(self.clean))
    def test_negative_origin(self): self.clean['annotations'][0]['bbox'][0]=-3;self.assertIn('NEGATIVE_ORIGIN',self.codes(self.clean))
    def test_bounds(self): self.clean['annotations'][0]['bbox'][0]=99;self.assertIn('OUT_OF_BOUNDS',self.codes(self.clean))
    def test_area(self): self.clean['annotations'][0]['area']=1;self.assertIn('AREA_MISMATCH',self.codes(self.clean))
    def test_invalid_area(self): self.clean['annotations'][0]['area']=-1;self.assertIn('INVALID_AREA',self.codes(self.clean))
    def test_duplicate_box(self): self.clean['annotations'].append(dict(self.clean['annotations'][0],id=2));self.assertIn('DUPLICATE_BOX',self.codes(self.clean))
    def test_empty_category(self): self.clean['categories'].append({'id':2,'name':'empty'});self.assertIn('EMPTY_CATEGORY',self.codes(self.clean))
    def test_md(self): self.assertIn('No issues detected',markdown(audit(self.clean)))
    def test_cli_clean(self): self.assertEqual(main([str(ROOT/'examples/clean.json')]),0)
    def test_cli_bad(self): self.assertEqual(main([str(ROOT/'examples/corrupt.json')]),2)
    def test_cli_missing(self): self.assertEqual(main(['/definitely/missing.json']),3)
    def test_deterministic(self): self.assertEqual(audit(self.clean),audit(self.clean))

if __name__=='__main__': unittest.main()
