from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,unittest,zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import compile_source,resource_audit,load,INSTALL_PREFIX
from gi_codec import encode as encode_gi,decode as decode_gi

class SourceTests(unittest.TestCase):
    def test_all_hashes_and_resource_references(self):
        files,configs=compile_source();expected=load(ROOT/'original-file-sha256.json')
        self.assertEqual({k:hashlib.sha256(v).hexdigest()for k,v in files.items()},expected)
        self.assertEqual(len(files),13)
        self.assertEqual(resource_audit(files,configs),{'cache_references_checked':10,'missing':[]})
        for path in(ROOT/'source/DATA/Interface').glob('*.json'):
            tree=load(path);self.assertEqual(decode_gi(encode_gi(tree)),tree,path.name)

    def test_pixel_edits_in_each_supported_representation(self):
        for name in ['2InvestA','2InvestN','OfferBtnN']:
            tree=load(ROOT/'source/DATA/Interface'/(name+'.json'))
            layer=tree['layers'][0]
            if tree['format']=='srhd-gi2-json-v1':
                packet=next(c for c in layer['commands']if 'pixels'in c);packet['pixels'][0]^=1
            else:layer['pixels'][0]^=1
            self.assertEqual(decode_gi(encode_gi(tree)),tree,name)

    def test_embedded_code_edit_is_used_by_the_build(self):
        original,_=compile_source()
        with tempfile.TemporaryDirectory()as folder:
            target=Path(folder);shutil.copytree(ROOT/'source',target/'source')
            path=target/'source/CFG/Rus/Lang.json';data=load(path);block=data['root']
            for name in ['Script','FHDBaseBuilderPaid','BeginOrder']:
                block=next(e['value']for e in block['entries']if e['kind']=='block'and e['name']==name)
            parameter=next(e for e in block['entries']if e['kind']=='parameter'and e['name']=='01')
            parameter['value']+=' // source edit test'
            path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
            files,_=compile_source(target)
        self.assertEqual([k for k in files if files[k]!=original[k]],['CFG/Rus/Lang.dat'])

    def test_source_only_build_has_no_prebuilt_dependencies(self):
        with tempfile.TemporaryDirectory()as folder:
            target=Path(folder)
            for name in ['scripts','source']:shutil.copytree(ROOT/name,target/name,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(ROOT/'original-file-sha256.json',target/'original-file-sha256.json')
            self.assertFalse(any(p.suffix in('.dat','.scr','.gi','.dll')for p in target.rglob('*')if p.is_file()))
            result=subprocess.run([sys.executable,str(target/'scripts/build.py'),'--strict-original'],cwd=target,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)
            expected=load(ROOT/'original-file-sha256.json')
            with zipfile.ZipFile(target/'dist/FHD_BaseBuilder_Paid_FROM_SOURCE.zip')as z:
                self.assertIsNone(z.testzip());self.assertEqual(len(z.namelist()),13)
                for name,digest in expected.items():self.assertEqual(hashlib.sha256(z.read(INSTALL_PREFIX+name)).hexdigest(),digest)

if __name__=='__main__':unittest.main()
