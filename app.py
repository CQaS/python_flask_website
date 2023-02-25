from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')


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
    return render_template('admin/libros.html')


@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    print(request.form['txtTitulo'])
    return redirect('/admin/libros')


if __name__ == '__main__':
    app.run(debug=True)
