import os
import threading
import asyncio
import sys
import time
from flask import Flask, jsonify
from main import StarTinG 

app = Flask(__name__)
PORT = int(os.environ.get('PORT', 5000))

# ग्लोबल वेरिएबल बॉट का स्टेटस चेक करने के लिए
bot_status = "Not Started"

def start_bot_core():
    global bot_status
    print("--- BOT THREAD STARTED ---")
    try:
        # यह लूप बॉट को क्रैश होने पर दोबारा चालू करेगा
        while True:
            print("Running StarTinG()...")
            bot_status = "Running"
            asyncio.run(StarTinG())
            print("Bot crashed or stopped! Restarting in 10 seconds...")
            bot_status = "Crashed/Restarting"
            time.sleep(10)
    except Exception as e:
        print(f"CRITICAL ERROR IN BOT THREAD: {e}")
        bot_status = f"Error: {str(e)}"
        sys.stdout.flush()

# --- महत्वपूर्ण बदलाव: Gunicorn के लिए थ्रेड को यहाँ स्टार्ट करें ---
# यह लाइन अब 'if __name__' के बाहर है ताकि Render इसे चला सके
try:
    if not os.environ.get("WERKZEUG_RUN_MAIN"): # यह सुनिश्चित करता है कि थ्रेड दो बार न चले
        bot_thread = threading.Thread(target=start_bot_core, daemon=True)
        bot_thread.start()
        print("Bot thread initiated via Global Scope")
except Exception as e:
    print(f"Error starting thread: {e}")

@app.route('/')
def health_check():
    return jsonify({
        "status": "Online", 
        "bot_internal_status": bot_status,
        "service": "Free Fire Bot Service"
    })

if __name__ == '__main__':
    # यह सिर्फ लोकल टेस्टिंग के लिए है
    print(f"Flask Web Server running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT)
