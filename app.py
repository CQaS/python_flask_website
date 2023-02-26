import os
from flask import Flask, render_template, request, redirect, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'crudnode'
mysql.init_app(app)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')


@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'), imagen)


@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')


@app.route('/admin/libros')
def admin_libros():

    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM libros')
    libros_list = cursor.fetchall()
    con.commit()
    con.close()

    return render_template('admin/libros.html', list_libros=libros_list)


@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():

    _titulo = request.form['txtTitulo']
    _Url = request.form['txtUrl']
    _Imagen = request.files['txtImagen']

    horaActual = datetime.now().strftime('%Y%H%M%S')
    cortado = _Imagen.filename.split('.')

    if _Imagen.filename != "":
        nombreNuevo = cortado[0] + '_' + horaActual + '.' + cortado[1]
        _Imagen.save('templates/sitio/img/' + nombreNuevo)

    query = "INSERT INTO `libros`(`id`, `titulo`, `url`, `imagen`) VALUES (NULL,%s,%s,%s)"
    datos = (_titulo, _Url, nombreNuevo)

    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query, datos)
    con.commit()
    con.close()

    return redirect('/admin/libros')


@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():

    _id = request.form['txtId']

    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute('SELECT imagen FROM libros WHERE id=%s', (_id))
    libro = cursor.fetchall()
    con.commit()

    if os.path.exists('templates/sitio/img/' + str(libro[0][0])):
        os.unlink('templates/sitio/img/' + str(libro[0][0]))

    query = "DELETE FROM libros WHERE id=%s"
    datos = (_id)

    cursor = con.cursor()
    cursor.execute(query, datos)
    con.commit()
    con.close()

    return redirect('/admin/libros')


if __name__ == '__main__':
    app.run(debug=True)
