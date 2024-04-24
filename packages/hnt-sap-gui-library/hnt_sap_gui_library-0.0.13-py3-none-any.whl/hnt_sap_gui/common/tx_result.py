class TxResult:
    def __init__(self, codigo, sbar) -> None:
        self.codigo = codigo
        self.sbar = sbar

    def __str__(self):
        return f"TxResult instance with codigo: '{self.codigo}', sbar: '{self.sbar}'"