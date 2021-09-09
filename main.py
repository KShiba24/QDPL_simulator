import numpy as np
from qdpl_simulator import QDPL_simulator
import matplotlib.pyplot as plt


simulator = QDPL_simulator()
Beta_list = [775, 439, 233, 77]
temp_list = [15, 80, 120, 150] # K

seed = 18

for i, j in zip(Beta_list, temp_list):
    print('Beta : {} = {}K'.format(i, j))
    simulator.initialize(seed=seed, h_percentage=60)
    simulator.run(max_epoch=300, temp=i, change_temp_to_end=False, plot_h_e=False)

    # plt.plot(np.mean(simulator.potential, axis=1))
    # plt.xlabel('iteration')
    # plt.ylabel('potential')
    # plt.show()
    # xx = np.arange(300)
    # pot = np.vstack((xx, np.mean(simulator.potential, axis=1))).T
    # np.savetxt('pot_{}.txt'.format(j), pot)
