from flask import Flask
from rotas.Home import Home_rota
from rotas.usuario import usuario_rota
from rotas.servico import servico_rota
from rotas.impostos import impostos_rota
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(Home_rota)
app.register_blueprint(usuario_rota,url_prefix='/usuario')
app.register_blueprint(servico_rota,url_prefix='/servico')
app.register_blueprint(impostos_rota,url_prefix='/impostos')
app.run(debug=True)
