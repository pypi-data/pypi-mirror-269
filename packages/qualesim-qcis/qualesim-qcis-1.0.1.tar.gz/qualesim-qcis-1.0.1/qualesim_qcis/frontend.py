from qualesim.plugin import *
from qualesim.host import *
from typing import List
from qualesim_qcis.QCIS_parser import QCISParser
from qualesim_qcis.QCIS_inst import QCISOpCode, QCISInst
from pathlib import Path
from qualesim_qcis.utils import QiDataStack
import math, cmath
import numpy as np


def ensure_path(fn) -> Path:
    assert isinstance(fn, (str, Path))
    if isinstance(fn, str):
        fn = Path(fn).resolve()
    return fn


@plugin("QCIS", "liu", "0.0.1")
class QCIS(Frontend):
    """QCIS frontend plugin. Must be implemented with the input *.qcis file"""

    # ==========================================================================
    # Init the plugin
    # ==========================================================================
    def __init__(self, filename, host_arb_ifaces=None, upstream_arb_ifaces=None):
        """Create the QCIS Frontend plugin with the input filename.

        Args:
            filename (*.qcis): filename is the input qi file to be simulated.
            host_arb_ifaces (_type_, optional): the argument is lists
            of strings representing the supported interface IDs. Defaults to None.
            upstream_arb_ifaces (_type_, optional): the argument is lists
            of strings representing the supported interface IDs. Defaults to None.
        """
        super().__init__(host_arb_ifaces, upstream_arb_ifaces)

        # use ensure_path to transform the str(filename) to Path(filename) and
        # read the file.
        fn = ensure_path(filename)
        with Path(fn).open("r") as f:
            data = f.read()

        # parse the QCIS Instrutions and store the instructions and names.
        self.parser: QCISParser = QCISParser()
        success, instructions, names = self.parser.parse(data)
        if success:
            self.instructions: List[QCISInst] = instructions
            self.qubit_names = names
        self.measure_qubit = []

    # ==========================================================================
    # Handle run the plugin
    # ==========================================================================
    def handle_run(self, **kwards):
        """Here is the handle_run function, it will control the simulation with
        different inputs.

        Args:
            **kwards: We use keyword parameters as input, now we have
                measure_mod="one_shot" and num_shots=int /
                measure_mod="state_vector" /
                measure_mod="Matrix" TODO

        Returns:
            ArbData: Return the ArbData to the upstream plugin. You can call the
            res with key-value form.
        """
        # determine whether to simulate the file based on the presence of the main function.
        try:
            # measure_mod default is one_shot and num_shots default is 1.
            measure_mod = "one_shot"
            if "measure_mod" in kwards.keys():
                measure_mod = kwards["measure_mod"]
            num_shots = 1
            if "num_shots" in kwards.keys():
                num_shots = kwards["num_shots"]
            # call the run_with_exemode with measure_mod and num_shots.
            arb = self.run_with_exemode(measure_mod, num_shots)
            return arb
        except:
            self.info("There is no start or error in simulator!")

    def run_with_exemode(self, measure_mod: str, num_shots=1):
        """Run the simulation with different exemode.
        if the measure_mod is one_shot, num_shots=2, the output is:
            {'quantum': (['q1', 'q2', 'q3'], [[1, 0, 0],
                                              [1, 0, 0]]),
            'classical': [{'c1': [1], 'c2': [0], 'c3': [0]},
                          {'c1': [1], 'c2': [0], 'c3': [0]}]}
            the classical result and quantum result is one-to-one correspondence.
        if the measure_mod is state_vector, the output is:
            {{['q1', 'q2', 'q3']:'[(0.4999999999999998+0j), 0j,
                                   (0.4999999999999998+0j), 0j,
                                   0j, (0.4999999999999998+0j),
                                   0j, (0.4999999999999998+0j)]'}}
        if the measure_mod is matrix, the output is:
            [{matrix1:[qubit_list1]}, {matrix2:[qubit_list2]}]

        Args:
            measure_mod (str): one_shot / state_vector / matrix
            num_shots (int, optional): if measure_mod = one_shot, num_shots would work.
            Defaults to 1.
            get_prob (bool): default False to accelerate the one_shot and state_vector's
            speed.

        Returns:
            arb (ArbData): Returns ArbData to the handle_run function.
        """
        # construct the output of different exemode.
        classical_value = []
        one_shot_value = []
        res: QiDataStack = self.function_run(measure_mod, num_shots)
        if (
            measure_mod == "one_shot"
            and len(res.one_shot) != num_shots
            and len(res.one_shot) == 1
        ):
            one_shot_value.append(res.one_shot[0])
            for i in range(num_shots - 1):
                res2: QiDataStack = self.function_run(measure_mod, num_shots)
                one_shot_value.append(res2.one_shot[0])
        else:
            one_shot_value = res.one_shot

        # construct one_shot exemodule
        one_shot = dict()
        one_shot["classical"] = classical_value
        one_shot["quantum"] = (res.res_qubit, one_shot_value)

        # construct state_vector exemodule
        state_vector = dict()
        state_vector["classical"] = res.cls_value
        state_vector["quantum"] = (self.qubit_names, res.state_vector)

        # output the result, Matrix is TODO
        if measure_mod == "one_shot":
            fn = one_shot
        elif measure_mod == "state_vector":
            fn = str(state_vector)
        elif measure_mod == "Matrix":
            fn = res.matrix_list
        else:
            fn = []
        arb = ArbData(res=fn)
        return arb

    def function_run(self, measure_mod="one_shot", num_shots=1):
        """Run the simulation

        Args:
            measure_mod (str): one_shot / state_vector / matrix
            num_shots (int, optional): if measure_mod = one_shot, num_shots would work.
            Defaults to 1.

        Returns:
            res (QiDataStack): res include the different output module of measure.
        """
        res: QiDataStack = QiDataStack()

        # prepare qubits
        qubit_list = dict()
        for i in self.qubit_names:
            qubit_list[i] = self.allocate(1)

        # store the qubit to be measured!
        msmt_qubits = []

        # conduct the simulation.
        for inst in self.instructions:
            # handle the single qubit operations.
            if inst.op_code.is_single_qubit_op():
                if inst.op_code == QCISOpCode.H:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            1 / math.sqrt(2),
                            1 / math.sqrt(2),
                            1 / math.sqrt(2),
                            -1 / math.sqrt(2),
                        ],
                    )
                    # self.h_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.X:
                    self.unitary(qubit_list[inst.qubit][0], [0, 1, 1, 0])
                    # self.x_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.X2P:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [i / (2**0.5) for i in [1, -1j, -1j, 1]],
                    )
                elif inst.op_code == QCISOpCode.X2M:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [i / (2**0.5) for i in [1, 1j, 1j, 1]],
                    )
                    # self.mx90_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.Y:
                    self.unitary(qubit_list[inst.qubit][0], [0, -1j, 1j, 0])
                    # self.y_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.Y2P:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [i / (2**0.5) for i in [1, -1, 1, 1]],
                    )
                    # self.y90_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.Y2M:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [i / (2**0.5) for i in [1, 1, -1, 1]],
                    )
                    # self.my90_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.Z:
                    self.unitary(qubit_list[inst.qubit][0], [1, 0.0, 0.0, -1])
                    # self.z_gate(qubit_list[inst.qubit][0])
                elif inst.op_code == QCISOpCode.S:
                    self.unitary(qubit_list[inst.qubit][0], [1, 0.0, 0.0, 1j])
                elif inst.op_code == QCISOpCode.SD:
                    self.unitary(qubit_list[inst.qubit][0], [1, 0.0, 0.0, -1j])
                elif inst.op_code == QCISOpCode.T:
                    self.unitary(
                        qubit_list[inst.qubit][0], [1, 0.0, 0.0, np.exp(1j * np.pi / 4)]
                    )
                elif inst.op_code == QCISOpCode.TD:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [1, 0.0, 0.0, np.exp(-1j * np.pi / 4)],
                    )
                elif inst.op_code == QCISOpCode.RX:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            np.cos(inst.altitude / 2),
                            -1j * np.sin(inst.altitude / 2),
                            -1j * np.sin(inst.altitude / 2),
                            np.cos(inst.altitude / 2),
                        ],
                    )
                    # self.rx_gate(qubit_list[inst.qubit][0], inst.altitude)
                elif inst.op_code == QCISOpCode.P:
                    a = cmath.exp(1.0j * inst.altitude)
                    self.unitary(qubit_list[inst.qubit][0], [1, 0, 0, a])
                elif inst.op_code == QCISOpCode.RY:
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            np.cos(inst.altitude / 2),
                            -np.sin(inst.altitude / 2),
                            np.sin(inst.altitude / 2),
                            np.cos(inst.altitude / 2),
                        ],
                    )
                    # self.ry_gate(qubit_list[inst.qubit][0], inst.altitude)
                elif inst.op_code == QCISOpCode.RZ:
                    self.unitary(
                        qubit_list[inst.qubit][0], [1, 0, 0, np.exp(1j * inst.azimuth)]
                    )
                    # self.rz_gate(qubit_list[inst.qubit][0], inst.azimuth)
                elif inst.op_code == QCISOpCode.RXY:
                    a = math.cos(0.5 * inst.altitude)
                    b = math.sin(0.5 * inst.altitude)
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            a,
                            -1.0j * cmath.exp(-1.0j * inst.azimuth) * b,
                            -1.0j * cmath.exp(1.0j * inst.azimuth) * b,
                            a,
                        ],
                    )
                elif inst.op_code == QCISOpCode.XY:
                    a = math.cos(0.5 * math.pi)
                    b = math.sin(0.5 * math.pi)
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            a,
                            -1.0j * cmath.exp(-1.0j * inst.azimuth) * b,
                            -1.0j * cmath.exp(1.0j * inst.azimuth) * b,
                            a,
                        ],
                    )
                elif inst.op_code == QCISOpCode.XY2P:
                    a = math.cos(0.25 * math.pi)
                    b = math.sin(0.25 * math.pi)
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            a,
                            -1.0j * cmath.exp(-1.0j * inst.azimuth) * b,
                            -1.0j * cmath.exp(1.0j * inst.azimuth) * b,
                            a,
                        ],
                    )
                elif inst.op_code == QCISOpCode.XY2M:
                    a = math.cos(-0.25 * math.pi)
                    b = math.sin(-0.25 * math.pi)
                    self.unitary(
                        qubit_list[inst.qubit][0],
                        [
                            a,
                            -1.0j * cmath.exp(-1.0j * inst.azimuth) * b,
                            -1.0j * cmath.exp(1.0j * inst.azimuth) * b,
                            a,
                        ],
                    )

            # handle the two qubit operations.
            elif inst.op_code.is_two_qubit_op():
                if inst.op_code == QCISOpCode.CZ:
                    self.unitary(
                        [qubit_list[inst.target_qubit][0]],
                        [
                            1.0,
                            0.0,
                            0.0,
                            -1.0,
                        ],
                        controls=[qubit_list[inst.control_qubit][0]],
                    )
                elif inst.op_code == QCISOpCode.CNOT:
                    self.unitary(
                        [qubit_list[inst.target_qubit][0]],
                        [
                            0.0,
                            1.0,
                            1.0,
                            0.0,
                        ],
                        controls=[qubit_list[inst.control_qubit][0]],
                    )
                    # self.cnot_gate(
                    #     qubit_list[inst.control_qubit][0],
                    #     qubit_list[inst.target_qubit][0],
                    # )
                elif inst.op_code == QCISOpCode.SWP:
                    self.unitary(
                        [
                            qubit_list[inst.control_qubit][0],
                            qubit_list[inst.target_qubit][0],
                        ],
                        [
                            1.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                            0.0,
                            0.0,
                            1.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                        ],
                    )
                    # self.swap_gate(
                    #     qubit_list[inst.control_qubit][0],
                    #     qubit_list[inst.target_qubit][0],
                    # )
                elif inst.op_code == QCISOpCode.SSWP:
                    self.unitary(
                        [
                            qubit_list[inst.control_qubit][0],
                            qubit_list[inst.target_qubit][0],
                        ],
                        [
                            1.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.5 + 0.5j,
                            0.5 - 0.5j,
                            0.0,
                            0.0,
                            0.5 - 0.5j,
                            0.5 + 0.5j,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                        ],
                    )
                    # self.sqswap_gate(
                    #     qubit_list[inst.control_qubit][0],
                    #     qubit_list[inst.target_qubit][0],
                    # )
                elif inst.op_code == QCISOpCode.ISWP:
                    self.unitary(
                        [
                            qubit_list[inst.control_qubit][0],
                            qubit_list[inst.target_qubit][0],
                        ],
                        [
                            1.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0j,
                            0.0,
                            0.0,
                            1.0j,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                        ],
                    )
                elif inst.op_code == QCISOpCode.SISWP:
                    self.unitary(
                        [
                            qubit_list[inst.control_qubit][0],
                            qubit_list[inst.target_qubit][0],
                        ],
                        [
                            1.0,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1 / math.sqrt(2),
                            1 / math.sqrt(2) * 1.0j,
                            0.0,
                            0.0,
                            1 / math.sqrt(2) * 1.0j,
                            1 / math.sqrt(2),
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.0,
                        ],
                    )
                elif inst.op_code == QCISOpCode.CP:
                    self.unitary(
                        qubit_list[inst.target_qubit][0],
                        np.diag([1, np.exp(1j * inst.azimuth)]),
                        qubit_list[inst.control_qubit][0],
                    )

            # handle the measure operation and add it to msmt_qubits.
            elif inst.op_code.is_measure_op():
                msmt_qubits.extend(
                    list(map(lambda q: qubit_list[q][0], inst.qubits_list))
                )
                for i in inst.qubits_list:
                    res.res_qubit.append(i)

        for j in self.qubit_names:
            if qubit_list[j][0] not in msmt_qubits:
                res.res_qubit_m.append(j)
        flag = 1
        if len(msmt_qubits) != 0:
            # PQInstr is short of "pure quantum instructions"
            self.measure(
                msmt_qubits,
                arb=ArbData(
                    measure_mod=measure_mod, num_shots=num_shots, typ="PQInstr"
                ),
            )
        else:
            flag = 0
            msmt_qubits = [qubit_list[self.qubit_names[0]][0]]
            self.measure(
                msmt_qubits,
                arb=ArbData(measure_mod="measureforres", typ="PQInstr"),
            )
        for j in res.res_qubit:
            a = self.get_measurement(qubit_list[j][0]).value
            res.cls_value[j] = a

        # store the result.
        if measure_mod == "state_vector":
            res.state_vector = eval(
                self.get_measurement(msmt_qubits[0])["state_vector_be"]
            )[1]
        else:
            res.state_vector = ""
        if flag:
            res.one_shot = self.get_measurement(msmt_qubits[0])["one_shot"]
        else:
            res.one_shot = [[]] * num_shots
        # free
        for i in self.qubit_names:
            self.free(qubit_list[i])
        return res
