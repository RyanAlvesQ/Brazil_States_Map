# 🌍 Projeto: Mapa Interativo com Flask e Leaflet

Este projeto exibe um mapa interativo onde o usuário pode selecionar um estado do Brasil e inserir seu nome. Os dados são enviados para um servidor Flask, que os armazena em um banco de dados PostgreSQL.

---

## 🚀 Como Executar o Projeto

### 1️⃣ **Instalar Dependências**

Certifique-se de ter o Python instalado (versão 3.11 ou superior).  
No terminal, crie uma venv execute:

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar o Banco de Dados

Configure os parâmetros no arquivo config/config.yaml (como host, usuário e senha do PostgreSQL).
Certifique-se de que o seu banco de dados PostgreSQL possua o database "states_map" e que esteja rodando.

### 3️⃣ Executar o Servidor Flask

Na raiz do projeto (source/), execute:
```bash
python app.py
```
O servidor estará disponível em:
👉 http://127.0.0.1:5000

### 4️⃣ Executar testes 

Na raiz do projeto (source/), execute:
pytest test/test_app.py

---

## 🎨 Tecnologias Utilizadas

   - Backend: Flask (Python)
   - Frontend: HTML, CSS, JavaScript, Leaflet.js
   - Banco de Dados: PostgreSQL
   - Outras Bibliotecas: Pandas, GeoPandas