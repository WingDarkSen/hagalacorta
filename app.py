from flask import Flask, request, redirect, render_template, jsonify, url_for
import sqlite3
import string, random

app = Flask(__name__)
DB = 'cortita.db'

def generar_codigo(longitud=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))

def conectar_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_original = request.form.get('url')
        if url_original:
            conn = conectar_db()
            codigo = generar_codigo()
            conn.execute('INSERT INTO urls (codigo, url_original) VALUES (?, ?)', (codigo, url_original))
            conn.commit()
            conn.close()
            return render_template('index.html', short_url=url_for('redirigir_corta', codigo=codigo))
    return render_template('index.html')

@app.route('/corta/<codigo>')
def redirigir_corta(codigo):
    conn = conectar_db()
    cur = conn.execute('SELECT url_original FROM urls WHERE codigo = ?', (codigo,))
    row = cur.fetchone()
    if row:
        conn.execute('UPDATE urls SET contador_clics = contador_clics + 1 WHERE codigo = ?', (codigo,))
        conn.commit()
        conn.close()
        return redirect(row['url_original'])
    return 'URL no encontrada', 404

@app.route('/api/estadisticas/<codigo>')
def estadisticas(codigo):
    conn = conectar_db()
    cur = conn.execute('SELECT codigo, url_original, fecha_creacion, contador_clics FROM urls WHERE codigo = ?', (codigo,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Código no encontrado'}), 404

#
#if __name__ == '__main__':
#    app.run(debug=True)
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
