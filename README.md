# 🌍 Project: Interactive Map with Flask and Leaflet  

This project displays an interactive map where users can select a state in Brazil and enter their name. The data is sent to a Flask server, which stores it in a PostgreSQL database.  

---

## 🚀 How to Run the Project

### 1️⃣ **Install Dependencies**

Make sure you have Python installed (version 3.11 or later).  
In the terminal, create a virtual environment and run:  

```bash
pip install -r requirements.txt
```

### 2️⃣ **Configure the Database**

Set the parameters in the config/config.yaml file (such as host, user, and PostgreSQL password).
Ensure that your PostgreSQL database contains the "states_map" database and is running.

### 3️⃣ **Run the Flask Server**

In the project root (source/), run:
```bash
python app.py
```
The server will be available at:
👉 http://127.0.0.1:5000

### 4️⃣ **Executar testes** 

In the project root (source/), run:
```bash
pytest test/test_app.py
```
---

## 🎨 Technologies Used

   - Backend: Flask (Python)
   - Frontend: HTML, CSS, JavaScript, Leaflet.js
   - Database: PostgreSQL
   - Other Libraries: Pandas, GeoPandas