import json
import os

DB_FILE = 'instance/db.json'

# Função para ler os dados do arquivo JSON
def read_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    return {"users": []}

# Função para salvar os dados no arquivo JSON
def write_data(data):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=2)
