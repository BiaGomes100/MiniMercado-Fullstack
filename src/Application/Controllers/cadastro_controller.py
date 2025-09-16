from Application.Service.cadastro_service import CadastroService

class CadastroCliente:
    def __init__(self):
        self.service = CadastroService()

    def criar(self, dados):
        return self.service.adicionar_cliente(
            dados["nome"],
            dados["cnpj"],
            dados["email"],
            dados["celular"],
            dados["senha"]
        )

    def listar(self):
        return self.service.listar_clientes()

    def ativar(self, cnpj):
        return self.service.ativar_cliente(cnpj)

    def inativar(self, cnpj):
        return self.service.inativar_cliente(cnpj)

    def atualizar(self, cnpj, dados):
        return self.service.atualizar_cliente(
            cnpj,
            nome=dados.get("nome"),
            email=dados.get("email"),
            celular=dados.get("celular"),
            senha=dados.get("senha"),
            status=dados.get("status")
        )

    def deletar(self, cnpj):
        return self.service.deletar_cliente(cnpj)
