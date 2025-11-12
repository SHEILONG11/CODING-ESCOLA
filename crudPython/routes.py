from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from datetime import datetime

def loadRoutes(app, init_csv, CSV_FILE):

    @app.route('/')
    def index():
        return render_template('myform.html')

    @app.route('/processar', methods=['POST'])
    def processar_formulario():
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        sexo = request.form.get('sexo')
        idade = request.form.get('idade')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        # você já tem data_hora no formulário mas você gera você mesmo:
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        if not nome or not idade:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('index'))

        try:
            init_csv()
            # usar pandas para ler + adicionar linha:
            df = pd.read_csv(CSV_FILE, encoding='utf-8')
            nova_linha = {
                'Nome': nome,
                'Email': email,
                'Telefone': telefone,
                'Sexo': sexo,
                'data_nascimento': idade,
                'Cidade': cidade,
                'Estado': estado,
                'Data/Hora': data_hora
            }
            df = df.append(nova_linha, ignore_index=True)
            df.to_csv(CSV_FILE, index=False, encoding='utf-8')

            flash(f'Dados de {nome} salvos com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao salvar dados: {str(e)}', 'error')
            return redirect(url_for('index'))

    @app.route('/visualizar')
    def visualizar_dados():
        try:
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE, encoding='utf-8')
            else:
                df = pd.DataFrame()  # vazio
            # converter para lista de listas para passar ao template
            dados = [list(df.columns)] + df.values.tolist()
            return render_template('dados.html', dados=dados)
        except Exception as e:
            flash(f'Erro ao carregar dados: {str(e)}', 'error')
            return redirect(url_for('index'))

    @app.route('/editar/<int:index>', methods=['GET', 'POST'])
    def editar_registro(index):
        if not os.path.exists(CSV_FILE):
            flash('Arquivo de dados não existe.', 'error')
            return redirect(url_for('visualizar_dados'))

        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        if index < 0 or index >= len(df):
            flash('Registro não encontrado.', 'error')
            return redirect(url_for('visualizar_dados'))

        if request.method == 'POST':
            for col in df.columns:
                df.at[index, col] = request.form.get(col)
            df.to_csv(CSV_FILE, index=False, encoding='utf-8')
            flash('Registro atualizado com sucesso!', 'success')
            return redirect(url_for('visualizar_dados'))

        # GET: renderizar formulário preenchido
        linha = df.iloc[index]
        return render_template('editar.html', header=list(df.columns), linha=linha, index=index)
    
