from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask import Blueprint

servico_rota = Blueprint('servico', __name__)

# Configuração do banco de dados
db_config2 = {
    'host':'mysql-1pqo.railway.internal',
    'user':'root',
    'password':'SnlardcVhxbNcFoGHtXSFKKeqCXKvfQO',
    'database':'railway',
}
@servico_rota.route('/servico', methods=['GET', 'POST'])
def servicos():
    if request.method == 'POST':
        # Recebendo os dados do formulário
        num_nota = request.form.get('num_nota')
        tomador = request.form.get('tomador')
        valor = request.form.get('valor')
        data_servico = request.form.get('data_servico')

        # Validação básica dos dados
        if not all([num_nota, tomador, valor, data_servico]):
            flash('Todos os campos são obrigatórios!')
            return redirect(url_for('servico'))

        try:
            # Conexão com o banco de dados
            db = mysql.connector.connect(**db_config2)
            cursor = db.cursor()
            
            # Inserindo os dados no banco de dados
            cursor.execute(
                "INSERT INTO servicos_cloud (num_nota, tomador, valor, data_servico) VALUES (%s, %s, %s, %s)", 
                (num_nota, tomador, valor, data_servico)
            )

            # Salvando as mudanças no banco
            db.commit()
            flash('Serviço registrado com sucesso!')
        
        except mysql.connector.Error as err:
            # Exibindo a mensagem de erro no caso de falha
            flash(f'Erro ao registrar o serviço: {err}')
        
        finally:
            # Fechando o cursor e a conexão
            cursor.close()
            db.close()

        return redirect(url_for('servico.lista_servicos',servicos=servicos))

    return render_template('servicos.html')




@servico_rota.route('/lista_servicos')
def lista_servicos():
    try:
        # Conexão com o banco de dados
        db = mysql.connector.connect(**db_config2)
        cursor = db.cursor(dictionary=True)
        
        # Executando a consulta para buscar os serviços
        cursor.execute("SELECT idservicos_cloud, num_nota, tomador, valor, data_servico FROM servicos_cloud")
        servicos = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f'Erro ao buscar os serviços: {err}')
        return redirect(url_for('servico.servicos'))
    
    finally:
        # Fechando o cursor e a conexão
        cursor.close()
        db.close()

    # Passando os serviços para o template
    return render_template('lista_servicos.html', servicos=servicos)

