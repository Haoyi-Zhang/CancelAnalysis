"""Negative controls and theorem-hypothesis regression checks; standard library only."""
from __future__ import annotations
import copy
import itertools
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import checker
ROOT=Path(__file__).resolve().parents[1]

class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=checker.load(ROOT/'cases/boolean-2-short-natural.json')
    def rejects(self,edit):
        c=copy.deepcopy(self.base);edit(c)
        with self.assertRaises((checker.Invalid,TypeError,KeyError,IndexError)):
            checker.audit(c)
    def test_valid_case(self):
        self.assertTrue(checker.audit(self.base)['locally_natural'])
    def test_missing_field(self):self.rejects(lambda c:c.pop('nodes'))
    def test_unknown_field(self):self.rejects(lambda c:c.update(extra=1))
    def test_bool_as_index(self):self.rejects(lambda c:c['inputs'].__setitem__(0,True))
    def test_domain_nonreflexive(self):self.rejects(lambda c:c['domains'][0]['leq'][0].__setitem__(0,0))
    def test_domain_nonantisymmetric(self):self.rejects(lambda c:c['domains'][0]['leq'][1].__setitem__(0,1))
    def test_domain_nontransitive(self):self.rejects(lambda c:c['domains'][0]['leq'][0].__setitem__(3,0))
    def test_nondistributive(self):
        # Five-element diamond M3: a genuine lattice, not distributive.
        r=[[int(a==b or a==0 or b==4) for b in range(5)] for a in range(5)]
        with self.assertRaisesRegex(checker.Invalid,'NONDISTRIBUTIVE'):
            checker.checked_order({'name':'M3','labels':list('01234'),'leq':r},checker.Budget())
    def test_duplicate_label(self):self.rejects(lambda c:c['domains'][0]['labels'].__setitem__(1,'0'))
    def test_label_type(self):self.rejects(lambda c:c['domains'][0]['labels'].__setitem__(1,{}))
    def test_bad_generator(self):self.rejects(lambda c:c['category']['generators'].append(0))
    def test_incomplete_generators(self):self.rejects(lambda c:c['category'].update(generators=[]))
    def test_bad_composition(self):self.rejects(lambda c:c['category']['composition'][0].__setitem__(0,1))
    def test_bad_identity(self):self.rejects(lambda c:c['category']['identities'].__setitem__(0,1))
    def test_program_vocabulary(self):self.rejects(lambda c:c['category']['programs'][0].insert(1,'multiply'))
    def insertion_category(self,target):
        return {'programs':[['entry','skip-2','skip-1','return'],target],
                'arrows':[[0,0],[0,1],[1,1]],'identities':[0,2],
                'generators':[1],
                'composition':[[0,None,None],[1,None,None],[None,1,2]]}
    def test_insertion_preserves_order(self):
        cat=self.insertion_category(['entry','skip-2','skip-3','skip-1','return'])
        self.assertEqual(checker.verified_category(cat,checker.Budget())[0],2)
    def test_reordering_is_not_insertion(self):
        cat=self.insertion_category(['entry','skip-1','skip-2','return'])
        with self.assertRaisesRegex(checker.Invalid,'NOT_SKIP_INSERTION'):
            checker.verified_category(cat,checker.Budget())
    def test_cycle(self):self.rejects(lambda c:c['nodes'][0]['inputs'].__setitem__(0,1))
    def test_table_truncation(self):self.rejects(lambda c:c['nodes'][0]['tables'][0].pop())
    def test_table_range(self):self.rejects(lambda c:c['nodes'][0]['tables'][0].__setitem__(0,4))
    def test_nonmonotone_operator(self):self.rejects(lambda c:c['nodes'][0]['tables'][0].__setitem__(0,3))
    def test_transport_identity(self):self.rejects(lambda c:c['transports'][0][0].__setitem__(0,1))
    def test_transport_composition(self):
        def edit(c):
            # Change a composite but leave its generator factors unchanged.
            a=c['category']['arrows'].index([0,3]);c['transports'][0][a]=[0,2,1,3]
        self.rejects(edit)
    def test_output_range(self):self.rejects(lambda c:c['outputs'].__setitem__(0,99))
    def test_probe_nonmonotone(self):self.rejects(lambda c:c['probes'][0]['tables'][0].__setitem__(0,2))
    def test_probe_nonnatural(self):
        c=checker.load(ROOT/'cases/nonidentity-transport.json')
        c['probes']=[{'wire':1,'tables':[[0,1,0,1]]}]
        with self.assertRaisesRegex(checker.Invalid,'NONNATURAL_PROBE'):checker.audit(c)
    def test_probe_type(self):self.rejects(lambda c:c['probes'][0]['tables'][0].__setitem__(0,False))
    def test_short_deadline(self):
        with self.assertRaisesRegex(checker.Invalid,'TIME_LIMIT'):checker.audit(self.base,seconds=-1)
    def test_json_duplicates(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'x';f.write_text('{"a":1,"a":2}')
            with self.assertRaisesRegex(checker.Invalid,'DUPLICATE_KEY'):checker.load(f)
    def test_json_nonfinite(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'x';f.write_text('{"a":NaN}')
            with self.assertRaisesRegex(checker.Invalid,'NONFINITE_JSON'):checker.load(f)
    def test_json_byte_cap(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'x';f.write_bytes(b' '*(checker.MAX_BYTES+1))
            with self.assertRaisesRegex(checker.Invalid,'BYTE_LIMIT'):checker.load(f)
    def test_forged_verdict(self):
        a=checker.audit(self.base)
        keys=['case','locally_natural','globally_natural','local_failures','global_failures','least_generator_witness']
        cert={k:a[k] for k in keys};cert['globally_natural']=False
        with self.assertRaisesRegex(checker.Invalid,'CERTIFICATE_MISMATCH'):checker.certificate(self.base,cert)
    def test_type_confused_certificate(self):
        a=checker.audit(self.base)
        keys=['case','locally_natural','globally_natural','local_failures','global_failures','least_generator_witness']
        cert={k:a[k] for k in keys};cert['local_failures']=False
        with self.assertRaisesRegex(checker.Invalid,'CERTIFICATE_MISMATCH'):checker.certificate(self.base,cert)
    def test_forged_witness(self):
        c=checker.load(ROOT/'cases/boolean-2-short-gauge.json');a=checker.audit(c)
        keys=['case','locally_natural','globally_natural','local_failures','global_failures','least_generator_witness']
        cert={k:a[k] for k in keys};cert['least_generator_witness']=None
        with self.assertRaisesRegex(checker.Invalid,'CERTIFICATE_MISMATCH'):checker.certificate(c,cert)
    def test_nested_closure_controls(self):
        for domain in ['boolean-2','boolean-3','anchored-boxes']:
            for mut in ['natural','mutated']:
                for obs in ['rank','flat']:
                    r=checker.audit(checker.load(ROOT/f'cases/closure-{domain}-{mut}-{obs}.json'))
                    self.assertTrue(r['nested_closure_pipeline'])
                    self.assertTrue(r['globally_natural'])
                    self.assertEqual(r['all_internal_probes_strict'],obs=='rank')
                    self.assertEqual(r['locally_natural'],mut=='natural')
                    self.assertEqual(r['probe_failures']>0,obs=='rank' and mut=='mutated')
    def test_nested_closure_forest_controls(self):
        for domain in ['boolean-2','boolean-3','anchored-boxes']:
            for mut in ['natural','mutated']:
                r=checker.audit(checker.load(ROOT/f'cases/closure-forest-{domain}-{mut}.json'))
                self.assertTrue(r['nested_closure_forest'])
                self.assertFalse(r['unary_pipeline'])
                self.assertTrue(r['all_internal_probes_strict'])
                self.assertTrue(r['globally_natural'])
                self.assertEqual(r['locally_natural'],mut=='natural')
                self.assertEqual(r['probe_failures']>0,mut=='mutated')
    def test_nesting_is_not_optional(self):
        r=checker.audit(checker.load(ROOT/'cases/non-nested-closure-control.json'))
        self.assertTrue(r['all_gates_closures']);self.assertFalse(r['nested_closure_pipeline'])
        self.assertTrue(r['globally_natural']);self.assertFalse(r['locally_natural'])
        self.assertEqual(r['probe_failures'],0)
    def test_coverage_is_joint(self):
        r=checker.audit(checker.load(ROOT/'cases/correlated-inputs.json'))
        self.assertEqual(r['input_coverage_at_object_zero'],[[2,4]])
        self.assertTrue(r['globally_natural']);self.assertFalse(r['locally_natural'])

class NonbijectiveTests(unittest.TestCase):
    def test_nonbijective_nested_natural(self):
        r=checker.audit(checker.load(ROOT/'cases/nonbijective-natural.json'))
        self.assertTrue(r['nested_closure_pipeline'])
        self.assertTrue(r['locally_natural'])
        self.assertEqual(r['probe_failures'],0)
    def test_nonbijective_visible(self):
        r=checker.audit(checker.load(ROOT/'cases/nonbijective-visible.json'))
        self.assertTrue(r['nested_closure_pipeline'])
        self.assertFalse(r['locally_natural'])
        self.assertGreater(r['probe_failures'],0)
    def test_nonidempotent_hidden(self):
        r=checker.audit(checker.load(ROOT/'cases/nonbijective-nonidempotent.json'))
        self.assertFalse(r['nested_closure_pipeline'])
        self.assertFalse(r['locally_natural'])
        self.assertEqual(r['probe_failures'],0)

if __name__=='__main__':unittest.main()
