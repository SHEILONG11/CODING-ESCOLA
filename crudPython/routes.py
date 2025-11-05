from flask import render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime

def loadRoutes(app, init_csv, CSV_FILE):
    
    @app.route('/')
    def index():
        return render_template('myform.html')

    # -------------------------
    # SALVAR FORMULÁRIO
    # -------------------------
    @app.route('/processar', methods=['POST'])
    def processar_formulario():
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        sexo = request.form.get('sexo')
        idade = request.form.get('idade')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')

        if not nome or not idade:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('index'))

        try:
            init_csv()
            novo_registro = pd.DataFrame([{
                'Nome': nome,
                'Email': email,
                'Telefone': telefone,
                'Sexo': sexo,
                'data_nascimento': idade,
                'Cidade': cidade,
                'Estado': estado,
                'Data/Hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }])

            # Se o arquivo existe, anexar; se não, criar
            if os.path.exists(CSV_FILE):
                novo_registro.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding='utf-8')
            else:
                novo_registro.to_csv(CSV_FILE, index=False, encoding='utf-8')

            flash(f'Dados de {nome} salvos com sucesso!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Erro ao salvar dados: {str(e)}', 'error')
            return redirect(url_for('index'))

    # -------------------------
    # VISUALIZAR DADOS
    # -------------------------
    @app.route('/visualizar')
    def visualizar_dados():
        try:
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE)
                dados = [df.columns.tolist()] + df.values.tolist()
            else:
                dados = []
            return render_template('dados.html', dados = dados)
        except Exception as e:
            flash(f'Erro ao carregar dados: {str(e)}', 'error')
            return redirect(url_for('index'))

    # -------------------------
    # EDITAR REGISTRO
    # -------------------------
    @app.route('/editar/<int:index>', methods=['GET', 'POST'])
    def editar_registro(index):
        if not os.path.exists(CSV_FILE):
            flash('Nenhum registro encontrado.', 'error')
            return redirect(url_for('visualizar_dados'))

        df = pd.read_csv(CSV_FILE)

        if index < 0 or index >= len(df):
            flash('Registro não encontrado.', 'error')
            return redirect(url_for('visualizar_dados'))

        if request.method == 'POST':
            try:
                for col in df.columns:
                    df.at[index, col] = request.form.get(col, df.at[index, col])
                df.to_csv(CSV_FILE, index=False, encoding='utf-8')
                flash('Registro atualizado com sucesso!', 'success')
                return redirect(url_for('visualizar_dados'))
            except Exception as e:
                flash(f'Erro ao atualizar: {e}', 'error')
                return redirect(url_for('visualizar_dados'))

        # GET → renderizar o formulário
        linha = df.iloc[index].tolist()
        header = df.columns.tolist()
        return render_template('editar.html', header=header, linha=linha, index=index)
