import sqlite3, os, base64, hashlib, secrets, io
from flask import Flask, request, render_template, redirect, session, flash, url_for, send_file, Response
from PIL import Image, ImageDraw, ImageFont

def db_connection():
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    return con

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

db = db_connection()
db.execute('drop table if exists users')
db.execute('drop table if exists fl4gz_1s_h3re')
db.execute('create table users (username text primary key, password text not null)')
db.execute('create table fl4gz_1s_h3re (fl4gz text not null)')
db.execute('insert into users values ("guest", "guest")')
db.execute('insert into users values ("admin", "admin")')
db.execute('insert into users values ("tabtabitabcat", "tabtabtab")')
db.execute('insert into fl4gz_1s_h3re values ("ARKAV{t4btab1tAb_bLacKboX_bl1ndSQli_C4ptcHa_ak4n_Ku_h4dap1_s3Muanya4}")')
db.commit()

d = lambda s: base64.b64decode(s).decode().replace(' ', '')

def generate_captcha():
    number = secrets.randbelow(9000) + 1000
    session['captcha'] = str(number)
    return hashlib.md5(str(number).encode()).hexdigest()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        captcha_md5 = generate_captcha()
        response = Response(render_template('login.html'))
        response.headers['X-CapCapiCap'] = captcha_md5 
        return response
    
    try:
        db = db_connection()
        username = d(request.form.get('username'))
        password = d(request.form.get('password'))
        captcha_input = request.form.get('captcha')

        if not captcha_input or captcha_input != session.get('captcha'):
            flash('Invalid CAPTCHA', 'danger')
            return redirect(url_for('login'))
        session.pop('captcha')
        query = f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
        logged_in = db.execute(query).fetchone()

        if logged_in:
            session['user'] = logged_in['username']
            return redirect(url_for('account'))

        flash('Invalid credentials', 'danger')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')

    return redirect(url_for('login'))

@app.route('/captcha.png')
def captcha_image():
    captcha_text = session.get('captcha', '0000')
    img = Image.new('RGB', (60, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_path = os.path.join("static", "Belanosima.ttf")
    try:
        font = ImageFont.truetype(font_path, 24)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2

    draw.text((text_x, text_y-8), captcha_text, fill=(0, 0, 0), font=font)
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/account')
def account():
    user = session.get('user')
    if user:
        return render_template('account.html')
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
