import os
from flask import Flask, request, jsonify, Blueprint
from Application.Controllers.cadastro_controller import CadastroCliente
from config.db import Base, engine
from Infrastructure.Model.cadastro_model import ClienteModel

Base.metadata.create_all(engine)

 

app = Flask(__name__)
cadastro_bp = Blueprint('cadastro_bp', __name__)
controller = CadastroCliente()


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


@cadastro_bp.route("/ativar/<string:cnpj>", methods=["PUT"])
def ativar_cliente(cnpj):
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


app.register_blueprint(cadastro_bp, url_prefix="/cadastro")

if __name__ == "__main__":
    app.run(debug=True)