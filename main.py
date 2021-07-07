from flask import Flask, Response , jsonify, request, render_template, session ,redirect
import pymongo
from bson.json_util import dumps
import bcrypt

app = Flask(__name__)
app.secret_key =b'l;a()2211'
try:
    mongo = pymongo.MongoClient(host='localhost',
                                port=27017,
                                serverSelectionTimeoutMs=100)
    mongo.server_info()
    db = mongo.notes
except:
    print("DB connection error")



@app.route('/')
def index():
    message = 'NOT LOGGED'
    if 'email' in session:
        message = session['email']
    return render_template('index.html', message=message)

@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == "GET":
        return render_template('registration.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        email_found = db.users.find_one({'email': email})

        if email_found:
            return 'Email already taken'
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'email': email,'password':hashed})
            return f'code {hashed}'

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return  render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        email_found = db.users.find_one({'email': email})

        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect('/')
            else:
                if "email" in session:
                    return redirect('/')
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Wrong email'
            return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    message =''
    if 'email' in session:
        message = 'logout'
        session.pop("email", None)
        return render_template("index.html",message=message)
    else:
        return render_template("index.html",message=message)



# @app.route('/user',methods=['POST'])
# def create_user():
#     user = {'name': request.form["name"],'age': request.form["age"]}
#     response = db.users.insert_one(user)
#     return jsonify({'message':'User created','id':f'{response.inserted_id}'})
#
# @app.route('/users', methods=['GET'])
# def list_users():
#     try:
#         data = dumps(db.users.find())
#         # for user in data:
#         #     user['_id'] = str(user['_id'])
#
#         return Response(response=data,status=200,mimetype='aplication/json')
#     except Exception as e:
#         print(e)



if __name__ == "__main__":
    app.run(debug=True)
