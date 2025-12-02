class VendaRealizada:
    def __init__(self, id_produto, quantidade_vendida, data_venda=None):
        self.id_produto = id_produto
        self.quantidade_vendida = quantidade_vendida
        self.data_venda = data_venda  # opcional, caso o banco já gere automaticamente

    def to_dict(self):
        return {
            "id_produto": self.id_produto,
            "quantidade_vendida": self.quantidade_vendida,
            "data_venda": str(self.data_venda) if self.data_venda else None
        }
