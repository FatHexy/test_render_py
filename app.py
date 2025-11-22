import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Konfigurasi API Key
# Di Render, kita akan set ini di menu Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("PERINGATAN: GEMINI_API_KEY belum disetting!")

# Konfigurasi Model (Gunakan gemini-1.5-flash agar cepat dan hemat)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"error": "API Key belum disetting di server."}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Pesan kosong"}), 400

    try:
        # Mengirim pesan ke Gemini
        response = model.generate_content(user_message)
        
        # Mengambil teks jawaban
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Gunicorn akan menangani port saat di deploy, ini hanya untuk lokal
    app.run(debug=True)