#digitarr no terminal: pip install flask
#para rodar: python main.py
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime
from routes import loadRoutes

app = Flask(__name__)
app.secret_key = 'puffy2020'  # Necessário para usar flash messages

# Nome do arquivo CSV
CSV_FILE = 'dados_pessoais.csv'

def init_csv():
    """Inicializa o arquivo CSV com cabeçalhos se não existir"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome','Email','Telefone','Sexo','data_nascimento','Cidade','Estado','Data/Hora'])


if __name__ == '__main__':
    loadRoutes(app,init_csv,CSV_FILE)
    app.run(debug=True)
    