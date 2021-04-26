from app import app

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret'
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)