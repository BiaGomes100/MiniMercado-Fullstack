from Application.Service.vendas_service import VendasService

class VendasController:
    def __init__(self):
        self.service = VendasService()

    # Registrar venda
    def registrar(self, cnpj, id_produto, dados):
        quantidade = dados.get("quantidade_vendida")
        resultado, status = self.service.registrar_venda(cnpj, id_produto, quantidade)
        return resultado, status

    # Listar vendas de um produto
    def listar_por_produto(self, id_produto):
        return self.service.listar_vendas_produto(id_produto)

    # Listar vendas de um seller
    def listar_por_seller(self, cnpj):
        return self.service.listar_vendas_seller(cnpj)

    # Cancelar venda
    def cancelar(self, venda_id):
        resultado, status = self.service.cancelar_venda_por_id(venda_id)
        return resultado, status
