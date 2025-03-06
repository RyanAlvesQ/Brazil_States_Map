from flask import Flask, jsonify, request, render_template
import geopandas as gpd

app = Flask(__name__)

# Carrega o shapefile (substitua pelo caminho correto do seu shapefile)
shapefile_path = "data/lml_unidade_federacao_a.shp"
gdf = gpd.read_file(shapefile_path)

# Converte os nomes dos estados para uma lista
estados = gdf["nome"].tolist()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estados", methods=["GET"])
def get_estados():
    return jsonify({"estados": estados})

@app.route("/estado", methods=["GET"])
def get_estado():
    estado_nome = request.args.get("nome")

    if not estado_nome:
        return jsonify({"error": "Nome do estado é obrigatório."}), 400

    estado = gdf[gdf["nome"] == estado_nome]

    if estado.empty:
        return jsonify({"error": "Estado não encontrado."}), 404

    return jsonify({
        "nome": estado_nome,
        "geojson": estado.to_json()
    })

if __name__ == "__main__":
    app.run(debug=True)
