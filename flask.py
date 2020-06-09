from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import mysql.connector

app = Flask(__name__)
app.secret_key="Hamtel575$"
sh=app.secret_key
db=mysql.connector.connect(host="localhost",user="root", password="",database="db1")
jwt = JWTManager(app)

@app.route("/signup", methods=["POST"])
def signup():
    '''Creating a signup Portal to add users'''

    sign=request.json
    username=sign['username']
    email=sign['email']
    password=sign['password']
    if username and email and password and request.method == "POST":
        make=generate_password_hash(password)
        code="INSERT INTO userdetail(name, email, password) VALUES(%s, %s, %s)"
        data=(username, email , make)
        cur=db.cursor()
        cur.execute(code, data)
        db.commit()
        cur.close()
        return jsonify(message= "Signup has been completed successfully")
    else:
        return jsonify(message="Please very each details")


@app.route("/Login", methods=["Post"])
def login():
    '''Creating a Login Portal and accessing tokens '''
    login=request.json
    user=login["username"]
    passprt=login["password"]
    if user and passprt and request.method =="POST":
        cur=db.cursor()
        cur.execute("SELECT name,password FROM userdetail WHERE name =%s",(user,) )
        row=cur.fetchone()
        cur.close()
        #print(row)
        if row[0] == user and check_password_hash(row[1],passprt):
            token=create_access_token(identity=user)
            return jsonify({"token":token})
        else:
            return jsonify(message="check your details"),400


@app.route("/add",methods=["POST"])
def add():
        temp=request.json
        country_name=temp['name']
        total_cases=temp['cases']
        total_recovered=temp['recovered']
        total_active=temp['active']
        gender=temp['gender']
        if country_name and total_cases and total_recovered and total_active and gender and request.method=="POST":
            set = "INSERT INTO covid(country, totalcase, recover, active, gender) VALUES(%s, %s, %s, %s, %s)"
            data = (country_name, total_cases, total_recovered, total_active, gender,)
            cur=db.cursor()
            cur.execute(set, data)
            db.commit()
            cur.close()
            return jsonify(message="Added Successfully"), 200

        else:
            return jsonify(message="Error occured"),400

@app.route("/country/<string:sha>")
@jwt_required
def country(sha):
    if sha==sh :
        cur=db.cursor()
        sql="SELECT * FROM covid"
        cur.execute(sql)
        result=cur.fetchall()
        cur.close()
        current_user = get_jwt_identity()
        return jsonify({"result":result,"user":current_user})
    else:
        return jsonify(message="Please provide secret key")


@app.route("/country/<int:id>")
def extract(id):
    cur=db.cursor()
    cur.execute("SELECT * FROM covid WHERE id=%s", (id,))
    result=cur.fetchone()
    return jsonify(result),200

@app.route("/update/<int:id>", methods=['PUT'])
@jwt_required
def update(id):
    
    temp = request.json
    country_name = temp['name']
    total_cases = temp['cases']
    total_recovered = temp['recovered']
    total_active = temp['active']
    gender = temp['gender']
    if country_name and total_cases and total_recovered and total_active and gender and request.method=="PUT":
        sql="UPDATE covid SET country=%s, totalcase=%s, recover=%s, active=%s, gender=%s WHERE id=%s"
        data=(country_name,total_cases,total_recovered,total_active,gender,id)
        cur=db.cursor()
        cur.execute(sql, data)
        db.commit()
        cur.close()
        return jsonify(message="Update has been successfuly saved")

@app.route("/Delete/<int:id>", methods=["DELETE"])
@jwt_required
def delete(id):
    
    data="YES"
    sql="UPDATE covid SET is_deleted = %s WHERE id=%s"
    data=(data,id)
    cur=db.cursor()
    cur.execute(sql,data)
    db.commit()
    cur.close()
    loginus=get_jwt_identity()
    return jsonify({"Deleted by":loginus})


if __name__ == "__main__":
    app.run(debug=True)
