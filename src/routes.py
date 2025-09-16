from flask import Flask, request, jsonify, Blueprint
from Application.Controllers.cadastro_controller import CadastroCliente

app = Flask(__name__)
cadastro_bp = Blueprint('cadastro_bp', __name__)
controller = CadastroCliente()

# Criar cliente
@cadastro_bp.route("/criar", methods=["POST"])
def criar_cliente():
    dados = request.get_json()
    novo_cliente = controller.criar(dados)
    return jsonify(novo_cliente), 201

# Listar clientes
@cadastro_bp.route("/listar", methods=["GET"])
def listar_clientes():
    clientes = controller.listar()
    return jsonify(clientes), 200

# Ativar cliente
@cadastro_bp.route("/ativar/<string:cnpj>", methods=["PUT"])
def ativar_cliente(cnpj):
    cliente = controller.ativar(cnpj)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404

# Inativar cliente
@cadastro_bp.route("/inativar/<string:cnpj>", methods=["PUT"])
def inativar_cliente(cnpj):
    cliente = controller.inativar(cnpj)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404

# Atualizar cliente
@cadastro_bp.route("/atualizar/<string:cnpj>", methods=["PUT"])
def atualizar_cliente(cnpj):
    dados = request.get_json()
    cliente = controller.atualizar(cnpj, dados)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404

# Deletar cliente
@cadastro_bp.route("/deletar/<string:cnpj>", methods=["DELETE"])
def deletar_cliente(cnpj):
    cliente = controller.deletar(cnpj)
    if cliente:
        return jsonify({"mensagem": f"Cliente {cliente['nome']} deletado com sucesso."}), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404

# Registrar Blueprint
app.register_blueprint(cadastro_bp, url_prefix="/cadastro")

if __name__ == "__main__":
    app.run(debug=True)
