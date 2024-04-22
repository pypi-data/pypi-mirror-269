import numpy as np

from PQAnalysis.topology.shakeTopology import ShakeTopologyGenerator
from PQAnalysis.core import Atom, AtomicSystem
from PQAnalysis.traj import Frame, Trajectory


class TestShakeTopologyGenerator:
    def test__init__(self):
        generator = ShakeTopologyGenerator()
        assert generator._atoms is None
        assert generator._use_full_atom_info is False

        generator = ShakeTopologyGenerator([Atom('C'), Atom('H')], True)
        assert generator._atoms == [Atom('C'), Atom('H')]
        assert generator._use_full_atom_info is True

        generator = ShakeTopologyGenerator(['C', 'H'])
        assert generator._atoms == [Atom('C'), Atom('H')]
        assert generator._use_full_atom_info is False

        generator = ShakeTopologyGenerator(np.array([0, 1]))
        assert np.allclose(generator._atoms, [0, 1])
        assert generator._use_full_atom_info is False

    def test_generate_topology(self):
        atoms = [Atom('C'), Atom('H'), Atom('H'), Atom('O'), Atom('H')]
        pos = np.array([[0.1, 0, 0], [1, 0, 0], [2.1, 0, 0],
                        [3, 0, 0], [4, 0, 0]])
        pos2 = np.array([[0.5, 0, 0], [1, 0.5, 0], [2.5, 0, 0],
                         [3, 0.5, 0], [4.5, 0, 0]])
        system = AtomicSystem(pos=pos, atoms=atoms)
        system2 = AtomicSystem(pos=pos2, atoms=atoms)

        traj = Trajectory([Frame(system), Frame(system2)])

        generator = ShakeTopologyGenerator(atoms=[Atom('H')])
        generator.generate_topology(traj)
        indices, target_indices, distances = generator.indices, generator.target_indices, generator.distances

        assert np.allclose(indices, [1, 2, 4])
        assert np.allclose(target_indices, [0, 3, 3])
        assert np.allclose(distances, [0.80355339, 0.80355339, 1.29056942])

    def test_average_equivalents(self):
        atoms = [Atom('C'), Atom('H'), Atom('H'), Atom('O'), Atom('H')]
        pos = np.array([[0.1, 0, 0], [1, 0, 0], [2.1, 0, 0],
                        [3, 0, 0], [4, 0, 0]])

        pos2 = np.array([[0.5, 0, 0], [1, 0.5, 0], [2.5, 0, 0],
                         [3, 0.5, 0], [4.5, 0, 0]])

        system = AtomicSystem(pos=pos, atoms=atoms)
        system2 = AtomicSystem(pos=pos2, atoms=atoms)

        traj = Trajectory([Frame(system), Frame(system2)])

        generator = ShakeTopologyGenerator(atoms=[Atom('H')])
        generator.generate_topology(traj)
        generator.average_equivalents([np.array([1]), np.array([2, 4])])

        indices, target_indices, distances = generator.indices, generator.target_indices, generator.distances

        assert np.allclose(indices, [1, 2, 4])
        assert np.allclose(target_indices, [0, 3, 3])
        assert np.allclose(distances, [0.80355339, 1.047061405, 1.047061405])

    def test_write_topology(self, capsys):
        atoms = [Atom('C'), Atom('H'), Atom('H'), Atom('O'), Atom('H')]
        pos = np.array([[0.1, 0, 0], [1, 0, 0], [2.1, 0, 0],
                        [3, 0, 0], [4, 0, 0]])

        pos2 = np.array([[0.5, 0, 0], [1, 0.5, 0], [2.5, 0, 0],
                         [3, 0.5, 0], [4.5, 0, 0]])

        system = AtomicSystem(pos=pos, atoms=atoms)
        system2 = AtomicSystem(pos=pos2, atoms=atoms)

        traj = Trajectory([Frame(system), Frame(system2)])

        generator = ShakeTopologyGenerator(atoms=[Atom('H')])
        generator.generate_topology(traj)

        print()
        generator.write_topology()

        captured = capsys.readouterr()
        assert captured.out == f"""
SHAKE 3  2  0
2 1 0.8035533905932739
3 4 0.8035533905932739
5 4 1.2905694150420948
END
"""
