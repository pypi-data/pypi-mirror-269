from enum import Enum, auto


class QCISOpCode(Enum):
    # The first single-qubit operation
    RZ = auto()
    XYARB = auto()
    XY = auto()
    XY2P = auto()
    XY2M = auto()
    X = auto()
    X2P = auto()
    X2M = auto()
    Y = auto()
    Y2P = auto()
    Y2M = auto()
    Z = auto()
    Z2P = auto()
    Z2M = auto()
    Z4P = auto()
    Z4M = auto()
    S = auto()
    SD = auto()
    T = auto()
    TD = auto()
    H = auto()
    P = auto()
    RX = auto()
    RY = auto()
    RXY = auto()
    # The last single-qubit operation

    # The first two-qubit operation
    CZ = auto()
    CNOT = auto()
    SWP = auto()
    SSWP = auto()
    ISWP = auto()
    SISWP = auto()
    CP = auto()
    FSIM = auto()
    # The last two-qubit operation with a parameter

    # The first measurement operation
    MEASURE = auto()
    M = auto()
    # The last measurement operation

    B = auto()

    def is_single_qubit_op(self):
        return self.RZ.value <= self.value <= self.RXY.value

    def is_two_qubit_op(self):
        return self.CZ.value <= self.value <= self.FSIM.value

    def is_measure_op(self):
        return self.MEASURE.value <= self.value <= self.M.value


class QCISInst(object):
    def __init__(self, op_code: QCISOpCode, **kwargs):
        """
        Data structure for representing QCIS instructions.

        Attributes:
            op_code: The operation code of the QCIS instruction.
            azimuth: The angle between the axis to rotate along and z-axis.
            altitude: The angle of rotation along a given axis.

        Single-qubit operation only attributes:
            qubit: The name string of target qubit.

        Two-qubit operation only attributes:
            control_qubit: The name string of control qubit.
            target_qubit: The name string of target qubit.

        Measurement operation only attributes:
            qubits_list: The names of all qubits to be measured.
        """
        self.op_code = op_code
        self.altitude = None
        self.azimuth = None
        self.control_qubit = None
        self.target_qubit = None
        self.qubit = None
        self.qubits_list = None
        self.handle_init(op_code, **kwargs)
        return

    def handle_init(self, op_code: QCISOpCode, **kwargs):
        """handle_init

        Args:
            op_code (QCISOpCode): the input operation
            kwargs : include qubits, altitude and azimuth

        Raises:
            ValueError: Found unrecognized opcode
        """
        # handle one qubit operation.
        if op_code.is_single_qubit_op():
            self.qubit = kwargs["qubit"]
            if "azimuth" in kwargs:
                self.azimuth = kwargs["azimuth"]
            if "altitude" in kwargs:
                self.altitude = kwargs["altitude"]
            return

        # handle two qubit operation.
        if op_code.is_two_qubit_op():
            self.control_qubit = kwargs["control_qubit"]
            self.target_qubit = kwargs["target_qubit"]
            if "azimuth" in kwargs:
                self.azimuth = kwargs["azimuth"]
            if "altitude" in kwargs:
                self.altitude = kwargs["altitude"]
            return

        # handle measure operation.
        if op_code.is_measure_op():
            # Should be a list even measuring only one qubit
            self.qubits_list = kwargs["qubits_list"]
            self.qubits_list.sort()
            return

        # handle B operation.
        if op_code == QCISOpCode.B:
            self.qubits_list = kwargs["qubits_list"]
            self.qubits_list.sort()
            return

        raise ValueError("Found unrecognized opcode: ", op_code)

    def __str__(self):
        if self.op_code.is_single_qubit_op():
            params_str = ""
            if self.azimuth is not None:
                params_str = params_str + ", azimuth: " + str(self.azimuth)
            if self.altitude is not None:
                params_str = params_str + ", altitude: " + str(self.altitude)
            return "Single-qubit op: {}, qubit: {}{}".format(
                self.op_code, self.qubit, params_str
            )

        if self.op_code.is_two_qubit_op():
            params_str = ""
            if self.azimuth is not None:
                params_str = params_str + ", azimuth: " + str(self.azimuth)
            if self.altitude is not None:
                params_str = params_str + ", altitude: " + str(self.altitude)
            return "Two-qubit op: {}, control: {}, target: {}{}".format(
                self.op_code, self.control_qubit, self.target_qubit, params_str
            )

        if self.op_code.is_measure_op():
            qubits_list_str = " ".join([qubit for qubit in self.qubits_list])
            return "Measure op: {}, qubits list: {}".format(
                self.op_code, qubits_list_str
            )

        raise ValueError("Unrecognized instruction.")

    def __eq__(self, other):
        # Two QCISInst instances with same values of attributes will be identical
        return self.__dict__ == other.__dict__
