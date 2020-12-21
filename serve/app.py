from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

# Criando o banco de dados com sqlalchemy
app = Flask(__name__, template_folder='templates')
# nome do banco db_produtos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_produtos.sqlite3'
db = SQLAlchemy(app)


#Criando o modelo do banco de dados
class Produtos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(100), nullable=False)
    quantidade = db.Column('quantidade', db.Integer, nullable=True)
    preco = db.Column('preco', db.Float, nullable=True)

    def __init__(self, id, nome, quantidade, preco):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def as_dict(self):
        return {c.nome: getattr(self, c.nome) for c in self.__table__.columns}


@app.route('/')
def index():
    produtos = []
    for produto in Produtos.query.all():
        produtos.append(produto.as_dict())
    return jsonify(produtos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        adic_produto = Produtos(request.form['id'],
                                request.form['nome'],
                                request.form['quantidade'],
                                request.form['preco'])
        db.session.add(adic_produto)
        #aqui salvamos o banco
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_produto = Produtos.query.get(id)
    if request.method == 'POST':
        edit_produto.id = request.form['id']
        edit_produto.nome = request.form['nome']
        edit_produto.quantidade = request.form['quantidade']
        edit_produto.preco = request.form['preco']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', edit_produto=edit_produto)


@app.route('/delete/<int:id>')
def delete(id):
    deleta_produto = Produtos.query.get(id)
    db.session.delete(deleta_produto)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

























