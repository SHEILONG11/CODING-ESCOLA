from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

#

def loadRoutes(app,init_csv,CSV_FILE):
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
            return render_template('dados.html', dados=dados)
        except Exception as e:
            flash(f'Erro ao carregar dados: {str(e)}', 'error')
            return redirect(url_for('index'))
        
    @app.route('/editar/<int:index>', methods=['GET', 'POST'])
    def editar_registro(index):
        # Ler todos os dados
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            dados = list(reader)
        # Cabeçalho
        header = dados[0]
        # Verificar se index válido
        try:
            linha = dados[index+1]  # +1 porque a linha 0 é o cabeçalho
        except IndexError:
            flash('Registro não encontrado.', 'error')
            return redirect(url_for('visualizar_dados'))

        if request.method == 'POST':
            # Para cada coluna, pegue o valor novo do form
            novos_valores = [ request.form.get(f'col_{j}') for j in range(len(header)) ]
            # Substituir no dados
            dados[index+1] = novos_valores
            # Gravar de volta
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(dados)
            flash('Registro atualizado com sucesso!', 'success')
            return redirect(url_for('visualizar_dados'))

        # GET: renderizar um formulário com valores preenchidos
        return render_template('editar.html', header=header, linha=linha, index=index)