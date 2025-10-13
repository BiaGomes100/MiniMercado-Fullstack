from Infrastructure.Model.cadastro_model import ClienteModel
from config.db import SessionLocal, Base, engine

# cria tabelas
Base.metadata.create_all(engine)

# cria sessão
session = SessionLocal()

# cria cliente
novo_cliente = ClienteModel(
    nome="Empresa Teste",
    cnpj="12345678000100",
    email="teste@empresa.com",
    celular="11999999999",
    senha="123456"
)

# adiciona no banco
session.add(novo_cliente)
session.commit()

# busca e imprime
clientes = session.query(ClienteModel).all()
for c in clientes:
    print(c.to_dict())

session.close()
