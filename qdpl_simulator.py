import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import trange

from qaa import QAA
from pot_h_e import *


class QDPL_simulator:
    def __init__(self):
        pass


    def initialize(self, seed=None, h_percentage=60, plot_h_e=False):
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

        if h_percentage!=int(h_percentage) or h_percentage>100 or h_percentage<0:
            raise Exception('h_percentage {%d} is wrong parameter' %h_percentage)
        else:
            self.h_percentage = h_percentage

        hole = np.array(([[x, y] for x in range(1,51,5) for y in range(1,51,5)]),dtype=float)
        hole = hole + np.random.randn(hole.shape[0], hole.shape[1])
        choi = np.random.choice(hole.shape[0], 100-self.h_percentage, replace=False)

        ele = hole[choi]
        hole = np.delete(hole, choi, axis=0)
        self.hole = hole
        self.ele = ele

        if plot_h_e:
            print('hole : {a}, ele : {b}'.format(a=hole.shape, b=ele.shape))
            plt.xlim(0,50)
            plt.ylim(0,50)
            plt.scatter(hole[:,0], hole[:,1])
            plt.scatter(ele[:,0], ele[:,1])
            plt.show()



    def run(self, tm=10, dt=0.1, max_epoch=300, e=2.0, reduc_para=0.97, temp=775, change_temp_to_end=False,
                plot_h_e=False, plot_potential=False, plot_histogram=True, find_good_seed=False):
        dist = []
        if plot_potential:
            dum = []

        qaa = [QAA(tm=10, dt=0.1, max_epoch=max_epoch) for i in range(self.h_percentage)]
        E = [0 for i in range(self.h_percentage)]
        self.potential = np.zeros((max_epoch, self.h_percentage))

        for k in trange(max_epoch):
            if plot_potential:
                pot = []

            pot_sum = np.zeros((self.hole.shape[0], self.hole.shape[0]))
            for j in range(self.hole.shape[0]):
                h_e_dist_vec, h_e_dist_sca = dist_e(self.hole[j], self.ele)
                h_h_dist_vec, h_h_dist_sca = dist_h_h(np.delete(self.hole, j, axis=0), self.hole[j])
                pot_h, diff_pot_h = potential_calc(h_h_dist_sca, h_h_dist_vec)
                pot_e, diff_pot_e = potential_calc(h_e_dist_vec, h_e_dist_vec)
                pot_sum = pot_h - pot_e

                if plot_potential:
                    pot.append(pot_sum)
                new_hole = self.hole[j] + diff_pot_h - diff_pot_e

                ener = qaa[j].update(k, pot_sum, temp)
                self.potential[k, j] = ener

                if k==0:
                    E[j] = ener
                    self.hole[j] = new_hole
                else:
                    if E[j] > ener:
                        self.hole[j] = new_hole
                        E[j] = ener
                    else:
                        self.hole[j] = self.hole[j]
                        E[j] = ener

                good_dist = h_e_dist_sca[np.where((0.53 < h_e_dist_sca) & (h_e_dist_sca < e))].tolist()
                if good_dist:
                    for gd in good_dist:
                        dist.append(gd)

                if self.hole[j][0] >= 50:
                    self.hole[j][0] = 0
                elif self.hole[j][0] <= 0:
                    self.hole[j][0] = 50
                elif self.hole[j][1] >= 50:
                    self.hole[j][1] = 0
                elif self.hole[j][1] <= 0:
                    self.hole[j][1] = 50
                else:
                    self.hole[j]= self.hole[j]


            if change_temp_to_end:
                temp *= reduc_para
            else:
                if k < 130:
                    temp *= reduc_para
                else:
                    temp *= 1

            if plot_potential:
                dum.append(np.sum(pot))

            if plot_h_e:
                print('temp : ', temp)
                plt.cla()
                plt.xlim(0,50)
                plt.ylim(0,50)
                plt.scatter(self.hole[:,0], self.hole[:,1])
                plt.scatter(self.ele[:,0], self.ele[:,1])
                plt.pause(0.1)

        if plot_h_e:
            plt.show()


        if plot_potential:
            plt.plot(dum)
            plt.show()


        if plot_histogram:
            sns.set_style("dark")
            sns.set_context("poster", 1, {"lines.linewidth": 4})
            sns.set_palette("dark")
            plt.xlabel("Bound radius[a.u.]")
            plt.xlim([0.4, 2.2])
            if dist:
                sns.distplot(dist, bins=30)
                plt.show()
            else:
                raise Exception('Excitons in effective range are not exist.')


        if find_good_seed:
            print('seed : {a} '.format(a=self.seed), end="")
            dist_min, dist_max = 0, 0
            if len(dist) != 0:
                for i in dist:
                    if i <= 1.0:
                        dist_min += 1
                    elif i >= 1.5:
                        dist_max += 1

                dist_min /= len(dist)
                dist_max /= len(dist)

            if 0.6 > dist_min > 0.2 and 0.6 > dist_max > 0.4 and dist_min < dist_max:
                print('o')
                return self.seed
            else:
                print('x')
