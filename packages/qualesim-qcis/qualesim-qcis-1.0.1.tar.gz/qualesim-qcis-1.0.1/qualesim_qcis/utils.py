class QiDataStack:
    def __init__(self) -> None:
        self.state_vector = None
        self.res_qubit = []
        self.res_qubit_m = []
        self.one_shot = []
        self.matrix_list = []
        self.cls_value = dict()
        self.PC = 0
