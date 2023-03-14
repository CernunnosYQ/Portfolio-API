from flask import Flask, jsonify, request
from flask_wtf import CSRFProtect
import os

from forms import SignUp


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = False
csfr = CSRFProtect(app)


@app.route('/')
def index():
    return jsonify(message='Hello World'), 200


@app.route('/auth/signup', methods=['POST'])
def signUp():
    signup = SignUp(request.form)

    if signup.validate():
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        return jsonify(email=email, password=password, username=username), 200
    
    return jsonify(success=False, message=signup.errors)


@app.route('/admin/post/')
@app.route('/admin/post/<id>')
def postForm(id = None):
    return jsonify(id=id), 200


if __name__ == '__main__':
    app.run(debug=True)