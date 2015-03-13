import numpy as np
import shutil
from os.path import join
from tempfile import mkdtemp
from unittest import TestCase, main

from pysph.base.utils import get_particle_array, get_particle_array_wcsph
from pysph.solver.utils import dump, load, dump_v1


class TestSolverUtils(TestCase):
    def setUp(self):
        self.root = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.root)

    def _get_filename(self, fname):
        return join(self.root, fname)

    def test_dump_and_load_works_by_default(self):
        x = np.linspace(0, 1.0, 10)
        y = x*2.0
        dt = 1.0
        pa = get_particle_array(name='fluid', x=x, y=y)
        fname = self._get_filename('simple.npz')
        dump(fname, [pa], solver_data={'dt': dt})
        data = load(fname)
        solver_data = data['solver_data']
        arrays = data['arrays']
        pa1 = arrays['fluid']
        self.assertListEqual(list(solver_data.keys()), ['dt'])
        self.assertListEqual(list(sorted(pa.properties.keys())),
                             list(sorted(pa1.properties.keys())))
        self.assertTrue(np.allclose(pa.x, pa1.x, atol=1e-14))
        self.assertTrue(np.allclose(pa.y, pa1.y, atol=1e-14))

    def test_dump_and_load_with_partial_data_dump(self):
        x = np.linspace(0, 1.0, 10)
        y = x*2.0
        pa = get_particle_array_wcsph(name='fluid', x=x, y=y)
        pa.set_output_arrays(['x', 'y'])
        fname = self._get_filename('simple.npz')
        dump(fname, [pa], solver_data={})
        data = load(fname)
        arrays = data['arrays']
        pa1 = arrays['fluid']
        self.assertListEqual(list(sorted(pa.properties.keys())),
                             list(sorted(pa1.properties.keys())))
        self.assertTrue(np.allclose(pa.x, pa1.x, atol=1e-14))
        self.assertTrue(np.allclose(pa.y, pa1.y, atol=1e-14))

    def test_dump_and_load_with_constants(self):
        x = np.linspace(0, 1.0, 10)
        y = x*2.0
        pa = get_particle_array_wcsph(name='fluid', x=x, y=y,
            constants={'c1': 1.0, 'c2': [2.0, 3.0]})
        pa.set_output_arrays(['x', 'y'])
        fname = self._get_filename('simple.npz')
        dump(fname, [pa], solver_data={})
        data = load(fname)
        arrays = data['arrays']
        pa1 = arrays['fluid']
        self.assertListEqual(list(sorted(pa.properties.keys())),
                             list(sorted(pa1.properties.keys())))
        self.assertListEqual(list(sorted(pa.constants.keys())),
                             list(sorted(pa1.constants.keys())))
        self.assertTrue(np.allclose(pa.x, pa1.x, atol=1e-14))
        self.assertTrue(np.allclose(pa.y, pa1.y, atol=1e-14))
        self.assertTrue(np.allclose(pa.c1, pa1.c1, atol=1e-14))
        self.assertTrue(np.allclose(pa.c2, pa1.c2, atol=1e-14))

    def test_load_works_with_dump_version1(self):
        x = np.linspace(0, 1.0, 10)
        y = x*2.0
        pa = get_particle_array(name='fluid', x=x, y=y)
        fname = self._get_filename('simple.npz')
        dump_v1(fname, [pa], solver_data={})
        data = load(fname)
        arrays = data['arrays']
        pa1 = arrays['fluid']
        self.assertListEqual(list(sorted(pa.properties.keys())),
                             list(sorted(pa1.properties.keys())))
        self.assertTrue(np.allclose(pa.x, pa1.x, atol=1e-14))
        self.assertTrue(np.allclose(pa.y, pa1.y, atol=1e-14))

    def test_that_output_array_information_is_saved(self):
        # Given
        x = np.linspace(0, 1.0, 10)
        y = x*2.0
        pa = get_particle_array(name='fluid', x=x, y=y, u=3*x)

        # When
        output_arrays = ['x', 'y', 'u']
        pa.set_output_arrays(output_arrays)
        fname = self._get_filename('simple.npz')
        dump(fname, [pa], solver_data={})
        data = load(fname)
        pa1 = data['arrays']['fluid']

        # Then.
        self.assertListEqual(pa.output_property_arrays, output_arrays)
        self.assertListEqual(pa1.output_property_arrays, output_arrays)

if __name__ == '__main__':
    main()
