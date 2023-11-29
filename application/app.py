from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# conexão com o banco de dados
app.config['MYSQL_HOST'] = '127.0.0.1' # 127.0.0.1 (localhost)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '147258369'
app.config['MYSQL_DB'] = 'contatos'

mysql_connection = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enviar_mensagem', methods=['GET', 'POST'])  
def enviar_mensagem():

    if request.method == 'POST':
        nome = request.form['nome']
        apelido = request.form['apelido']
        email = request.form['email']
        crush = request.form['crush']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        cur = mysql_connection.cursor()

        cur.execute("INSERT INTO recados(nome, apelido, email, crush, assunto, mensagem) VALUES (%s, %s, %s, %s, %s, %s)", (nome, apelido, email, crush, assunto, mensagem))

        mysql_connection.commit()

        cur.close()

        return redirect(url_for('ler_mensagens'))
    
    return render_template('enviar-mensagem.html')



# LEITURA DE DADOS DO MYQSL PARA O SITE
@app.route('/ler_mensagens')  
def ler_mensagens():
    cur = mysql_connection.cursor()

    mensagens = cur.execute("SELECT * FROM recados")

    if mensagens > 0:
        dados_mensagens = cur.fetchall()
        cur.close()

        i = 0
        detalhes_mensagens = []
        for msg in dados_mensagens:
            accordion = ["accordionExample"+str(i), "#collapse"+str(i), "collapse"+str(i), "#accordionExample"+str(i)]
            detalhes_mensagens.append(accordion + list(msg))
            i += 1

        return render_template('ler-mensagens.html', detalhes_mensagens=detalhes_mensagens)
    else:
        cur.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
