from flask import Flask, jsonify, request, render_template
import geopandas as gpd
from config.config_reader import ConfigReader
from config.db_config import Connection
from repository.database_operator import DatabaseOperations 

app = Flask(__name__)

# Lendo a configuração do YAML
config_reader = ConfigReader()
app_config = config_reader.read_config("./config/config.yaml")
params = app_config.get('configuration_parameters', [])

def get_params(param_name):
    return next((param.get(param_name) for param in params if param_name in param), None)

# Parâmetros do banco de dados
db_host = get_params("database_host")
db_port = get_params("database_port")
db_name = get_params("database_name")
db_user = get_params("database_user")
db_password = get_params("database_password")

# Caminho do shapefile
shapefile_path = get_params("shapefile_path")

# Carrega o shapefile
gdf = gpd.read_file(shapefile_path)
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

@app.route("/salvar_dados", methods=["POST"])
def salvar_dados():
    """
    Recebe o nome do usuário e o estado selecionado e insere no banco de dados.
    """
    data = request.get_json()
    nome_usuario = data.get("nome")
    mapa_selecionado = data.get("estado")

    if not nome_usuario or not mapa_selecionado:
        return jsonify({"error": "Nome do usuário e estado são obrigatórios."}), 400

    try:
        # Conectando ao banco de dados
        connection = Connection.db_connection(db_host, db_port, db_name, db_user, db_password)
        if connection is None:
            return jsonify({"error": "Erro ao conectar ao banco de dados."}), 500

        # Instanciando a classe de operações no banco de dados
        db_operations = DatabaseOperations()

        db_operations.create_tables(connection)
        
        # Inserindo os dados
        result = db_operations.insert_data(connection, nome_usuario, mapa_selecionado)

        if "Erro" in result:
            return jsonify({"error": result}), 500

        return jsonify({"mensagem": "Dados salvos com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao salvar os dados: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
