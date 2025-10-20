#digitarr no terminal: pip install flask
#para rodar: python main.py
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

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

@app.route('/')
def index():
    return render_template('myform.html')

@app.route('/processar', methods=['POST'])
def processar_formulario():
    # Obter dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    sexo = request.form.get('sexo')
    idade = request.form.get('idade')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    data_hora = request.form.get('data_hora')
    
    # Validar se todos os campos foram preenchidos
    if not nome or not idade:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('index'))
    
    try:
        # Converter idade e altura para números
        '''idade = int(idade)#inteiro'''
        
        
        # Validar faixas de valores
        '''if nome < 0 or nome > 200:
            flash('Nome deve estar entre 0 e 120 caracteres!', 'error')
            return redirect(url_for('index'))
            
        if email < 0 or email > 250:
            flash('Email deve estar entre 0 e 250 caracteres!', 'error')
            return redirect(url_for('index'))'''
        
        # Inicializar CSV se necessário
        init_csv()
        
        # Adicionar dados ao CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            writer.writerow([nome,email,telefone,sexo,idade,cidade,estado,data_hora])
        
        flash(f'Dados de {nome} salvos com sucesso!', 'success')
        return redirect(url_for('index'))
        
    except ValueError:
        flash('Por favor, insira valores numéricos válidos para nome!', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erro ao salvar dados: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/visualizar')
def visualizar_dados():
    """Página para visualizar os dados salvos"""
    try:
        dados = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                dados = list(reader)
        return render_template('dados2.html', dados=dados)
    except Exception as e:
        flash(f'Erro ao carregar dados: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    