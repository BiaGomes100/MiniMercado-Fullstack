from Infrastructure.Model.produto_model import ProdutoModel
from config.db import SessionLocal, Base, engine

# cria tabelas
Base.metadata.create_all(engine)

# cria sessão
session = SessionLocal()

# cria produto
novo_produto = ProdutoModel(
    seller_id=1,
    nome="Feijão Carioca 1kg",
    preco=8.50,
    quantidade=100,
    status=True,
    imagem="feijao.png"
)

# adiciona no banco
session.add(novo_produto)
session.commit()

# busca e imprime
produtos = session.query(ProdutoModel).all()
for p in produtos:
    print(p.to_dict())

session.close()
