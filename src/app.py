from flask import Flask
from flask_cors import CORS
from controller.contacts import contacts_bp
import database

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(contacts_bp, url_prefix="/contacts")

@app.route('/')
def home():
    return "Contacts Backend Running Successfully!"

if __name__ == "__main__":
    database.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
