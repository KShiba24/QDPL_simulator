import numpy as np


def dist_e(hole, ele):
    r = []
    for i in range(ele.shape[0]):
        r.append((hole - ele[i]).tolist())

    r_a_1 = np.array(r).reshape(-1,2)
    r_a_2 = np.sqrt(r_a_1[:,0]**2 + r_a_1[:,1]**2)
    return r_a_1, r_a_2


def dist_h_h(hole, ob_hole):
    r = hole - ob_hole
    r1 = np.sqrt(r[:, 0]**2 + r[:, 1]**2)
    return r, r1


def potential_calc(r1, r2, full=False):
    if full:
        potential = 1.602/(4 * np.pi * 8.8541 * (abs(r1)+0.53))
    else:
        potential = np.sum(1.602/(4 * np.pi * 8.8541 * (abs(r1)+0.53)**2))

    diff_potential = 1.602/(4 * np.pi * 8.8541 * (abs(r2)+0.53)**3)
    diff_potential = np.sum(diff_potential, axis=0)
    return potential, diff_potential
