from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "minhachavesecretaqueninguemfazideia"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///esportes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Esportes(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    modalidade = db.Column(db.String(80), nullable=False)
    categoria = db.Column(db.String(40))
    federacao = db.Column(db.String(80))
    olimpico = db.Column(db.Boolean, default=False, nullable=False)
    expoente = db.Column(db.String(40))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    esportes = Esportes.query.order_by(Esportes.uid).all()
    return render_template("index.html", esportes=esportes)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar_esporte():
    if request.method == "POST":
        esporte = Esportes(
            nome=request.form["nome"],
            modalidade=request.form["modalidade"],
            categoria=request.form.get("categoria"),
            federacao=request.form.get("federacao"),
            olimpico=request.form.get("olimpico") == "True",
            expoente=request.form.get("expoente"),
        )
        db.session.add(esporte)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("cadastraesporte.html")


@app.route("/editar/<int:uid>", methods=["GET", "POST"])
def editar_esporte(uid):
    esporte = Esportes.query.get_or_404(uid)

    if request.method == "POST":
        esporte.nome = request.form["nome"]
        esporte.modalidade = request.form["modalidade"]
        esporte.categoria = request.form.get("categoria")
        esporte.federacao = request.form.get("federacao")
        esporte.olimpico = request.form.get("olimpico") == "True"
        esporte.expoente = request.form.get("expoente")

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("editar_esporte.html", esporte=esporte)


@app.route("/excluir/<int:uid>", methods=["POST"])
def excluir_esporte(uid):
    esporte = Esportes.query.get_or_404(uid)
    db.session.delete(esporte)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
