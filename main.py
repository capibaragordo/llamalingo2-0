from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    clave = request.form['clave']

    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("SELECT nombre FROM usuarios WHERE correo=? AND clave=?", (correo, clave))
    datos = cur.fetchone()
    con.close()

    if datos:
        session['usuario'] = datos[0]
        return redirect(url_for('menu'))
    else:
        return render_template('login.html', error="Correo o contraseña incorrecta")


@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('home'))
    return render_template('menu.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']

        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nombre, correo, clave) VALUES (?, ?, ?)", (nombre, correo, clave))
        con.commit()
        con.close()

        flash("✅ Cuenta creada correctamente. Ahora inicia sesión.")
        return redirect(url_for('home'))

    return render_template('registro.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    nombre = session.get('usuario', 'Anónimo')  # si no ha iniciado sesión, se muestra como Anónimo
    mensaje = request.form['comentario']

    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("INSERT INTO comentarios (nombre, mensaje) VALUES (?, ?)", (nombre, mensaje))
    con.commit()
    con.close()

    return "✅ Comentario recibido correctamente"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
