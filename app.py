from flask import Flask, render_template, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

ARQUIVO_DADOS = "sistema_ponto.json"


def carregar_dados():

    if not os.path.exists(ARQUIVO_DADOS):

        return {
            "usuarios": {},
            "registros": []
        }

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(dados):

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:

        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    dados = carregar_dados()

    info = request.json

    nome = info.get("nome")
    digital = info.get("digital")

    if digital in dados["usuarios"]:

        return jsonify({
            "status": "erro",
            "mensagem": "Digital já cadastrada!"
        })

    dados["usuarios"][digital] = nome

    salvar_dados(dados)

    return jsonify({
        "status": "sucesso",
        "mensagem": f"{nome} cadastrado com sucesso!"
    })


@app.route("/bater_ponto", methods=["POST"])
def bater_ponto():

    dados = carregar_dados()

    info = request.json

    digital = info.get("digital")

    if digital in dados["usuarios"]:

        nome = dados["usuarios"][digital]

        agora = datetime.datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        registro = {
            "nome": nome,
            "digital": digital,
            "horario": agora
        }

        dados["registros"].append(registro)

        salvar_dados(dados)

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Ponto registrado para {nome}",
            "horario": agora
        })

    else:

        return jsonify({
            "status": "erro",
            "mensagem": "Digital não encontrada!"
        })


@app.route("/listar_registros")
def listar_registros():

    dados = carregar_dados()

    return jsonify(dados["registros"])


if __name__ == "__main__":
    app.run(debug=True)