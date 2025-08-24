class Cadastro:
    def __init__(self, nome, cnpj, email, celular, senha, status= "Inativo"):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email 
        self.celular = celular 
        self.senha = senha 
        self.status = status
        
    def to_dict(self):         
        return {
            "nome" : self.nome,
            "cnpj" : self.cnpj,
            "email" : self.email,
            "celular" : self.celular,
            "senha" : self.senha,
            "status" : self.status
        }
