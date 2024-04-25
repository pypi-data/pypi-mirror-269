import pytest
import numpy as np
from molSimplify.Classes.mol3D import mol3D
from molSimplify.Scripts.geometry import rotate_around_axis
from molSimplify.Scripts.rmsd import rigorous_rmsd, quaternion_rotate
from scipy.spatial.transform import Rotation


@pytest.mark.parametrize(
    'path1,path2,ref_hungarian,ref_none',
    [['example_1_noff', 'example_1', 0.3991, 0.7749],
     ['BUWGOQ', 'BUWGOQ_final', 2.43958, 0.49113],
     ['BUWGOQ_noH', 'BUWGOQ_noH_final', 1.74814, 0.11826],
     ['BUWGOQ', 'BUWGOQ_final_reordered', 2.43958, 3.02598]]
    )
def test_rigorous_rmsd(resource_path_root, path1, path2, ref_hungarian, ref_none, atol=1e-3):
    # Reference values calculated using https://pypi.org/project/rmsd/
    # >>> calculate_rmsd --reorder path1.xyz path2.xyz
    # >>> calculate_rmsd path1.xyz path2.xyz
    xyz_1 = resource_path_root / "inputs" / "rmsd" / f"{path1}.xyz"
    mol1 = mol3D()
    mol1.readfromxyz(xyz_1)

    xyz_2 = resource_path_root / "inputs" / "rmsd" / f"{path2}.xyz"
    mol2 = mol3D()
    mol2.readfromxyz(xyz_2)

    r = rigorous_rmsd(mol1, mol2, reorder='hungarian')
    assert abs(r - ref_hungarian) < atol

    r = rigorous_rmsd(mol1, mol2, reorder='none')
    assert abs(r - ref_none) < atol


@pytest.mark.skip
def test_methane_rotation(atol=1e-3):
    """This test case is intended to show the problem with our current RMSD implementation"""
    # XYZ data copied from
    # https://github.com/OpenChemistry/avogadrodata/blob/master/data/methane.xyz
    d = 1.02672
    theta = 110 * np.pi / 180
    xyz_string = (
        "C      0.00000    0.00000    0.0000\n"
        "H      0.00000    0.00000    1.08900\n"
        "H      1.02672    0.00000   -0.36300\n"
        f"H    {d * np.cos(theta):8.5f}   {d * np.sin(theta):8.5f}   -0.36300\n"
        f"H    {d * np.cos(theta):8.5f}   {-d * np.sin(theta):8.5f}   -0.36300\n"
    )
    mol1 = mol3D()
    mol1.readfromstring(xyz_string)

    mol2 = mol3D()
    mol2.readfromstring(xyz_string)
    # rotate 180 degrees around the z axis
    mol2 = rotate_around_axis(mol2, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 180)
    assert rigorous_rmsd(mol1, mol2, reorder='none') < atol

    assert rigorous_rmsd(mol1, mol2, reorder='hungarian') < atol


def test_quaternion_rotate(atol=1e-3):
    rot_mat = Rotation.from_rotvec(np.array([1., 2., 3.])).as_matrix()
    x = np.array([[1.2, 0., 0.],
                  [0., 0., 0.],
                  [0.5, 0.9, 0.]])
    y = x @ rot_mat

    np.testing.assert_allclose(quaternion_rotate(x, y), rot_mat, atol=atol)
