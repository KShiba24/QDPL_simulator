from qiskit import QuantumCircuit, Aer, execute
import numpy as np

class QAA:
    def __init__(self, bn=2, tm=10, dt=0.1, max_epoch=300):
        self.tm = tm
        self.dt = dt
        self.bn = bn
        self.max_epoch = max_epoch
        self.backend = Aer.get_backend('statevector_simulator')

        qc = QuantumCircuit(self.bn)
        for i in range(self.bn):
            qc.h(i)
        self.vector = execute(qc, self.backend).result().get_statevector()


    def _rx(self, qci, theta, q):
        qci.u3(theta, -np.pi / 2, np.pi / 2, q)


    def _rz(self, qci, phi, q):
        qci.u1(phi, q)


    def _rzz(self, qci, phi, q1, q2):
        qci.cx(q1, q2)
        self._rz(qci, -2.0 * phi, q2)
        qci.cx(q1, q2)


    def update(self, idx, J, hx):
        qc = QuantumCircuit(self.bn)
        qc.set_statevector(self.vector)
        s = idx / self.max_epoch
        for i in range(self.bn):
            self._rx(qc, 2.0 * hx * self.dt, i)
            for j in range(i + 1, self.bn):
                self._rzz(qc, J * self.dt, i, j)

        vec = execute(qc, self.backend).result().get_statevector()
        self.vector = vec
        a = list(np.abs(vec)).index(max(np.abs(vec)))
        solution = list(format(a, '02b'))
        solution = [int(i) for i in solution]

        E = J * solution[0] * solution[1]
        return E
