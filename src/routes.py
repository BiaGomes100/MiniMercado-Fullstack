import os
from flask import Flask, request, jsonify, Blueprint
from Application.Controllers.cadastro_controller import CadastroCliente
from Application.Controllers.login_controller import Login_Controller
from config.db import Base, engine
from Infrastructure.Model.cadastro_model import ClienteModel
from Application.Controllers.produto_controller import ProdutoController
from Application.Controllers.vendas_controller import VendasController
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
cadastro_bp = Blueprint('cadastro_bp', __name__)
Produto_bp = Blueprint('Produto_bp', __name__)
Login_bp = Blueprint("Login_bp", __name__)
controller = CadastroCliente()
Vendas_bp = Blueprint("Vendas_bp", __name__)
vendas_controller = VendasController().vendas_controller


@cadastro_bp.route("/criar", methods=["POST"])
def criar_cliente():
    dados = request.get_json()
    resultado = controller.criar(dados)
    return jsonify(resultado), 201


@cadastro_bp.route("/verificar/<string:cnpj>", methods=["POST"])
def verificar_cliente(cnpj):
    dados = request.get_json()
    token = dados.get("token")
    resultado = controller.verificar(cnpj, token)
    return jsonify(resultado), 200


@cadastro_bp.route("/listar", methods=["GET"])
def listar_clientes():
    clientes = controller.listar()
    return jsonify(clientes), 200


@cadastro_bp.route("/ativar", methods=["PUT"])
def ativar_cliente():
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    cliente = controller.ativar(cnpj)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404


@cadastro_bp.route("/inativar/<string:cnpj>", methods=["PUT"])
def inativar_cliente(cnpj):
    cliente = controller.inativar(cnpj)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404


@cadastro_bp.route("/atualizar/<string:cnpj>", methods=["PUT"])
def atualizar_cliente(cnpj):
    dados = request.get_json()
    cliente = controller.atualizar(cnpj, dados)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404


@cadastro_bp.route("/deletar/<string:cnpj>", methods=["DELETE"])
def deletar_cliente(cnpj):
    cliente = controller.deletar(cnpj)
    if cliente:
        return jsonify({"mensagem": "Cliente removido com sucesso", "cliente": cliente}), 200
    return jsonify({"erro": "Cliente não encontrado"}), 404

#parte dos produtos


produto_controller = ProdutoController()


@Produto_bp.route("/adicionar", methods=["POST"])
def adicionar_produto():
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    return jsonify(produto_controller.criar(cnpj ,dados)), 201

@Produto_bp.route("/listar/<string:cnpj>", methods=["GET"])
def listar_produtos(cnpj):
    return jsonify(produto_controller.listar(cnpj)) 

@Produto_bp.route("/detalhar/<int:id>", methods=["GET"])
def detalhar_produto(id):
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    return jsonify(produto_controller.detalhar(cnpj, id)), 200

@Produto_bp.route("/atualizar", methods=["PUT"])
def atualizar_produto():
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    id = dados.get("id_produto")
    return jsonify(produto_controller.atualizar(cnpj, id, dados)), 200

@Produto_bp.route("/inativar/<int:id>", methods=["PUT"])
def inativar_produto(id):
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    return jsonify(produto_controller.inativar(cnpj, id)), 200

@Produto_bp.route("/vender/<int:id>", methods=["POST"])
def vender_produto(id):
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    return jsonify(produto_controller.vender(cnpj, id, dados)), 201


#Login

login_controller = Login_Controller()

@Login_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    resultado, status = login_controller.login(dados)
    return jsonify(resultado), status


#vendas 

@Vendas_bp.route("/registrar/<int:id_produto>", methods=["POST"])
def registrar_venda(id_produto):
    dados = request.get_json()
    cnpj = dados.get("cnpj")
    resultado, status = vendas_controller.registrar(cnpj, id_produto, dados)
    return jsonify(resultado), status

@Vendas_bp.route("/listar/produto/<int:id_produto>", methods=["GET"])
def listar_vendas_produto(id_produto):
    vendas = vendas_controller.listar_por_produto(id_produto)
    return jsonify(vendas), 200

@Vendas_bp.route("/listar/seller/<string:cnpj>", methods=["GET"])
def listar_vendas_seller(cnpj):
    vendas = vendas_controller.listar_por_seller(cnpj)
    return jsonify(vendas), 200

@Vendas_bp.route("/cancelar/<int:venda_id>", methods=["DELETE"])
def cancelar_venda(venda_id):
    resultado, status = vendas_controller.cancelar(venda_id)
    return jsonify(resultado), status



app.register_blueprint(cadastro_bp, url_prefix="/cadastro")
app.register_blueprint(Produto_bp, url_prefix="/produto")
app.register_blueprint(Login_bp, url_prefix ="/login")
app.register_blueprint(Vendas_bp, url_prefix="/vendas")

if __name__ == "__main__":
    app.run(debug=True)