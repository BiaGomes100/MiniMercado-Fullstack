class ClienteModel:
    def __init__(self, id, nome, cnpj, email, celular, senha, status, criado_em):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha
        self.status = status
        self.criado_em = criado_em

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "senha": self.senha,
            "status": self.status,
            "criado_em": self.criado_em
        }
