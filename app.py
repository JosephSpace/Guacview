import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import os
from functools import wraps
from api import get_system_stats
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', False)
app.secret_key = 'guacview-secret-key'

# Aktif kullanıcıları takip etmek için global değişken
active_users = {}
# Kullanıcı oturumlarının geçerlilik süresi (dakika)
SESSION_TIMEOUT = 30

# Kullanıcının giriş yapmış olup olmadığını kontrol eden decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

# Active Directory yapılandırması
AD_SERVER = 'your-ad-server.com'  # AD sunucu adresi
AD_DOMAIN = 'your-domain.com'  # AD domain adı
AD_BASE_DN = 'DC=your-domain,DC=com'  # AD base DN

# Active Directory kimlik doğrulama fonksiyonu
def authenticate_ad(username, password):
    # Geçici test hesabı için debug mod kontrolü
    if app.debug and username == 'admin' and password == '123':
        return True

    if app.debug and username == 'test' and password == '123':
        return True
    
    try:
        # AD sunucusuna bağlanma
        server = Server(AD_SERVER, get_info=ALL)
        
        # Kullanıcı adını domain formatına çevirme
        user_dn = f'{username}@{AD_DOMAIN}'
        
        # Kimlik doğrulama
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM)
        if conn.bind():
            # Kullanıcı bilgilerini arama
            search_filter = f'(sAMAccountName={username})'
            conn.search(AD_BASE_DN, search_filter, search_scope=SUBTREE, attributes=['cn', 'givenName', 'sn', 'mail'])
            
            if len(conn.entries) > 0:
                return True
        return False
    except Exception as e:
        print(f"AD Authentication Error: {e}")
        return False
    finally:
        try:
            if 'conn' in locals() and conn.bound:
                conn.unbind()
        except:
            pass

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    error = None
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Active Directory kimlik doğrulama
        if authenticate_ad(username, password):
            session['username'] = username
            # Kullanıcıyı aktif kullanıcılar listesine ekleyelim
            active_users[username] = datetime.now()
            return redirect(url_for('index'))
        else:
            error = 'Geçersiz kullanıcı adı veya şifre. Lütfen Active Directory hesabınızla giriş yapın.'
    
    return render_template('login.html', form=form, error=error)

@app.route('/connections')
@login_required
def connections():
    return render_template('table.html')

@app.route('/applications')
@login_required
def applications():
    return render_template('applications.html')

# Eski yönlendirmeler için route'lar
@app.route('/4-site/Dashboard/dashboard.html')
def old_dashboard():
    return redirect(url_for('dashboard'))

@app.route('/1-Guac-Dashboard/main.html')
def old_dashboard_beta():
    return redirect(url_for('dashboard'))

@app.route('/2-Guac-Login/index.html')
def old_login():
    return redirect(url_for('login'))

@app.route('/3-Guac-Table/index.html')
def old_connections():
    return redirect(url_for('connections'))

@app.route('/1.5-Guac-Search/index.html')
def old_search():
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    username = session.get('username')
    if username and username in active_users:
        # Kullanıcıyı aktif kullanıcılar listesinden çıkaralım
        active_users.pop(username, None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/api/system-stats')
@login_required
def system_stats():
    return jsonify(get_system_stats())

@app.route('/api/active-connections')
@login_required
def active_connections_count():
    # Süresi dolmuş oturumları temizleyelim
    current_time = datetime.now()
    expired_users = []
    for username, last_activity in active_users.items():
        if (current_time - last_activity) > timedelta(minutes=SESSION_TIMEOUT):
            expired_users.append(username)
    
    # Süresi dolmuş kullanıcıları listeden çıkaralım
    for username in expired_users:
        active_users.pop(username, None)
    
    # Mevcut kullanıcının son aktivite zamanını güncelleyelim
    current_user = session.get('username')
    if current_user:
        active_users[current_user] = current_time
    
    # Aktif kullanıcı sayısını döndürelim
    return jsonify({'active_connections': len(active_users)})

# Çalışan uygulamaları takip etmek için global değişken
running_applications = {}

@app.route('/api/start-application', methods=['POST'])
@login_required
def start_application():
    data = request.json
    app_id = data.get('app_id')
    app_path = data.get('app_path')
    
    if not app_id or not app_path:
        return jsonify({'success': False, 'error': 'Uygulama ID ve yolu gereklidir'})
    
    try:
        # Python dosyası mı kontrol edelim
        is_python_file = app_path.lower().endswith('.py')
        
        # Uygulamayı başlatalım
        if is_python_file:
            # Python dosyasını CMD'de çalıştır
            process = subprocess.Popen(
                ['cmd.exe', '/c', 'start', 'python', app_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            # Flask uygulaması için varsayılan IP adresini belirliyoruz (örneğin, localhost:5000)
            flask_url = None
            if app_id == "1":  # Birinci uygulama Flask ise (örneğin app.py)
                flask_url = "http://192.168.1.121:5000"  # Varsayılan Flask portu
        else:
            # .exe dosyalarını normal şekilde çalıştır
            process = subprocess.Popen(app_path, shell=True)
            flask_url = None
        
        # Çalışan uygulamalar listesine ekleyelim
        running_applications[app_id] = {
            'process': process,
            'path': app_path,
            'start_time': datetime.now()
        }
        
        # HTML dosyası var mı kontrol edelim
        html_path = None
        app_dir = os.path.dirname(app_path)
        for file in os.listdir(app_dir):
            if file.endswith('.html'):
                html_path = os.path.join(app_dir, file)
                break
        
        # Flask URL'sini ekleyelim (varsa)
        response_data = {
            'success': True, 
            'message': f'Uygulama başlatıldı: {app_path}',
            'html_path': html_path
        }
        if flask_url:
            response_data['flask_url'] = flask_url
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop-application', methods=['POST'])
@login_required
def stop_application():
    data = request.json
    app_id = data.get('app_id')
    
    if not app_id:
        return jsonify({'success': False, 'error': 'Uygulama ID gereklidir'})
    
    if app_id not in running_applications:
        return jsonify({'success': False, 'error': 'Uygulama çalışmıyor'})
    
    try:
        # Uygulamayı durduralım
        process = running_applications[app_id]['process']
        process.terminate()
        
        # Çalışan uygulamalar listesinden çıkaralım
        running_applications.pop(app_id, None)
        
        return jsonify({'success': True, 'message': f'Uygulama durduruldu: {app_id}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='192.168.1.121', port=3000, debug=True)