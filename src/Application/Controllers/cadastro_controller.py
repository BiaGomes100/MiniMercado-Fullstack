from Domain.cadastro import Cadastro

class CadastroCliente:
    def __init__(self):
        self.Cadastro_cliente = [] #armazana os cadastros
        
        
    def adicionarCliente (self, nome, cnpj, email, celular, senha):  #essa função pega o cadastro do mercado e adicona em uma lista
        novo = Cadastro(nome , cnpj, email, celular, senha)
        self.Cadastro_cliente.append(novo)
        return novo

    
    def atualizarPerfil(self, nome=None, cnpj=None, email=None, celular=None, senha=None, status=None):
        try:
            if nome: self.nome = nome
            if cnpj: self.cnpj = cnpj
            if email: self.email = email
            if celular: self.celular = celular
            if senha: 
                if len(senha) < 4:
                    raise ValueError("Senha muito curta!")
                self.__senha = senha       #senha mais protegida 
            if status: self.status = status
        except ValueError as senha:
            print(f"Erro ao atualizar perfil: {senha}")
    
    
    def cadastroAtivo(self):
        self.status = "Ativo"


    def cadastroInativo(self):
        self.status = "Inativo"


    def listarCliente(self):
        return self.Cadastro_cliente
    
    def deletar_cliente(self, cnpj):
        try:
            cliente_removido = self.Cadastro_cliente.pop(cnpj)
            return {"mensagem": f"Cliente {cliente_removido.nome} deletado com sucesso."}
        except IndexError:
            return {"erro": "Cliente não encontrado"}


    