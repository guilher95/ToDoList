from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db'
db = SQLAlchemy(app)


class Tarea(db.Model):  # vinculamos los objetos con la base de datos directamente
    __tablename__ = "tarea"
    id = db.Column(db.Integer, primary_key=True)  # identificador unico de cada tarea(con primary# key)
    contenido = db.Column(db.String(200))  # contenido de tarea
    completada = db.Column(db.Boolean)


db.create_all()  # creamos las tablas
db.session.commit()  # ejecucion de las tareas pendientes de la base de datos


@app.route('/')
def home():
    todas_las_tareas= Tarea.query.all()  #recuperamos el contenido de la db y la redenrizamos
    return render_template("indext.html",lista_de_tareas=todas_las_tareas)


@app.route('/crear-tarea', methods=['POST'])
def crear():
    tarea = Tarea(contenido=request.form['contenido_tarea'], completada=False) #pasamos el input del html por aqui
    db.session.add(tarea)  # añadimos el objeto a la base de datos
    db.session.commit()
    return redirect(url_for('home'))   #nos redirecciona a home

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea=Tarea.query.filter_by(id=int(id)).delete() #filtramos los datos por el id y el que coincida con el parametro aportado por la ruta se elimina
    db.session.commit()
    return redirect(url_for('home')) #redireccion a home con la pagina refrescado no aparecerá la tarea eliminada

@app.route('/tarea-completada/<id>')
def completada(id):
    tarea = Tarea.query.filter_by(id=int(id)).first() #obtenemos la terea que se busca
    tarea.completada = not(tarea.completada)          #guardamos la variable booleana
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

