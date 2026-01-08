from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'elyse_secret_key_123' 

def init_db():
    with sqlite3.connect('hafatra.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hafatra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anarana TEXT, 
                email TEXT, 
                hafatra TEXT,
                daty TEXT,
                valiny TEXT
            )
        ''')
        columns = [column[1] for column in cursor.execute('PRAGMA table_info(hafatra)')]
        if 'daty' not in columns:
            cursor.execute('ALTER TABLE hafatra ADD COLUMN daty TEXT')
        if 'valiny' not in columns:
            cursor.execute('ALTER TABLE hafatra ADD COLUMN valiny TEXT')
        conn.commit()

init_db()

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['fr', 'en']:
        session['language'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route('/')
def home():
    lang = session.get('language', 'fr')
    return render_template('index.html', lang=lang)

@app.route('/momba')
def momba():
    lang = session.get('language', 'fr')
    return render_template('momba.html', lang=lang)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'elyse27' and password == 'Thony#Randry207':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_backend'))
        else:
            return render_template('login.html', soso_kevitra="Identifiants invalides !")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin-backend')
def admin_backend():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    with sqlite3.connect('hafatra.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, anarana, email, hafatra, daty, valiny FROM hafatra ORDER BY id DESC')
        tahiry = cursor.fetchall()
    hafatra_rehetra = [{'id': h[0], 'anarana': h[1], 'email': h[2], 'hafatra': h[3], 'daty': h[4], 'valiny': h[5]} for h in tahiry]
    return render_template('admin.html', hafatra_rehetra=hafatra_rehetra)

@app.route('/hamaly/<int:id>', methods=['POST'])
def hamaly_hafatra(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    valiny = request.form.get('valiny')
    with sqlite3.connect('hafatra.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE hafatra SET valiny = ? WHERE id = ?', (valiny, id))
        conn.commit()
    return redirect(url_for('admin_backend'))

@app.route('/andefa-hafatra', methods=['POST'])
def handefa_hafatra():
    anarana = request.form.get('anarana')
    email = request.form.get('email')
    hafatra = request.form.get('hafatra')
    ora_izao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    with sqlite3.connect('hafatra.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO hafatra (anarana, email, hafatra, daty) VALUES (?, ?, ?, ?)', 
                       (anarana, email, hafatra, ora_izao))
        conn.commit()
    
    lang = session.get('language', 'fr')
    return render_template('index.html', lang=lang, fahombiazana=f"Merci {anarana} !")

@app.route('/hamafa/<int:id>')
def hamafa_hafatra(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    with sqlite3.connect('hafatra.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM hafatra WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('admin_backend'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)