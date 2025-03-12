import pytest
import psycopg2
import json
import sys
import os
import logging
from datetime import datetime

# Criar diretório para logs se não existir
LOG_DIR = "test_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Criar nome do arquivo de log baseado na data e hora
log_filename = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Configuração de logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para exibir no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Handler para salvar no arquivo
file_handler = logging.FileHandler(log_filename, mode='w')  # 'w' para sobrescrever a cada execução
file_handler.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Adicionar handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Adiciona o diretório 'source' ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from config.db_config import Connection
from repository.database_operator import DatabaseOperations
from config.config_reader import ConfigReader

# Obtém o caminho absoluto do arquivo de configuração
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

# Carregar as configurações do banco de dados para testes
config_reader = ConfigReader()

try:
    app_config = config_reader.read_config(CONFIG_PATH)
    params = app_config.get('configuration_parameters', [])
except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo de configuração não encontrado: {CONFIG_PATH}")

def get_params(param_name):
    return next((param.get(param_name) for param in params if param_name in param), None)

DB_TEST_CONFIG = {
    "host": get_params("database_host"),
    "port": get_params("database_port"),
    "dbname": get_params("database_name"),
    "user": get_params("database_user"),
    "password": get_params("database_password"),
}

@pytest.fixture(scope="function")
def db_connection():
    """Cria e retorna uma conexão com o banco de testes."""
    conn = psycopg2.connect(**DB_TEST_CONFIG)
    
    # Criar a tabela se não existir
    db_operations = DatabaseOperations()
    db_operations.create_tables(conn)

    yield conn  # Fornece a conexão para os testes

    conn.close()

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_salvar_dados(client, db_connection):
    """Testa se os dados do usuário são inseridos corretamente no banco de dados."""
    payload = {
        "nome": "Ryan",
        "estado": "São Paulo"
    }
    
    logger.info(f"🟡 Enviando dados para salvar: {payload}")  
    response = client.post("/salvar_dados", data=json.dumps(payload), content_type="application/json")
    
    logger.info(f"🟢 Status da resposta: {response.status_code}")
    logger.info(f"🟢 Resposta: {response.json}")

    assert response.status_code == 201
    assert response.json["mensagem"] == "Dados salvos com sucesso!"

    # Verificar se os dados foram realmente inseridos no banco
    cursor = db_connection.cursor()
    cursor.execute("SELECT nome_usuario, mapa_selecionado FROM MAP.Map_infos WHERE nome_usuario = %s;", ("Ryan",))
    user_data = cursor.fetchone()

    logger.info(f"🟢 Dados recuperados do banco: {user_data}")

    assert user_data == ("Ryan", "São Paulo")

    # Remover os dados inseridos no teste sem apagar os registros reais
    cursor.execute("DELETE FROM MAP.Map_infos WHERE nome_usuario = %s;", ("Ryan",))
    db_connection.commit()

    logger.info(f"🔴 Dados de {payload['nome']} removidos após o teste.")
