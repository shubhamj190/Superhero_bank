# importing all the necessary files
from flask import Flask, request, render_template,redirect,url_for, make_response
import pymysql

app = Flask(__name__)
# --------------------------Dashboard--------------------------------------------
@app.route('/')
def home():
    if request.authorization and request.authorization.username =='username' and request.authorization.password =='password':
        # return render_template('index.html')

        servername = "localhost"
        username = "root"
        password = ""
        dbname = "superhero_bank"

        try:	
            db = pymysql.connect(servername, username, password, dbname)
            c = db.cursor()
            query = "select * from customer"
            c.execute(query)
            data = c.fetchall()
            return render_template('index.html', row=data)

        except Exception:
            return "Failed to connect"


    return make_response('could not verify',401,{'WWW-Authenticate':"Basic realm='Login Required'"})

# --------------------------Dashboard--------------------------------------------


# --------------------------form--------------------------------------------


@app.route('/form',methods=['GET','POST'])
def entryForm():
   return render_template('form.html')

# --------------------------form--------------------------------------------


# --------------------------insert--------------------------------------------
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":

        Account = request.form['Account']
        Name = request.form['Name']
        Address = request.form['Address']
        Mobile = request.form['Mobile']
        Balance = request.form['Balance']
        # Photo = request.form['Photo']

        servername = "localhost"
        username = "root"
        password = ""
        dbname = "superhero_bank"

        try:
            db = pymysql.connect(servername, username, password, dbname)
            c = db.cursor()
            query = "insert into customer(Account, Name, Address, Mobile, Balance)values ('{}','{}','{}','{}','{}')".format( Account, Name, Address, Mobile, Balance)
            c.execute(query)
            db.commit()
            # return 'all is ok'
            return redirect(url_for('home'))

        except Exception:

            db.rollback()
            return "Failed to connect"
# --------------------------insert--------------------------------------------


# --------------------------Delete--------------------------------------------

@app.route('/delete/<rid>')  # this shit is done
def delete(rid):

    servername = "localhost"
    username = "root"
    password = ""
    dbname = "superhero_bank"

    try:
        db = pymysql.connect(servername, username, password, dbname)
        c = db.cursor()
        query = "delete from customer where Account='{}'".format(rid)
        c.execute(query)
        db.commit()
        return redirect(url_for('home'))

    except Exception:
        db.rollback()
        return "Failed to delete"

# --------------------------Delete--------------------------------------------


# --------------------------edit--------------------------------------------

@app.route('/edit/<rid>')
def edit(rid):

    servername = "localhost"
    username = "root"
    password = ""
    dbname = "superhero_bank"

    try:
        db = pymysql.connect(servername, username, password, dbname)
        c = db.cursor()
        query = "select * from customer where Account={}".format(rid)
        c.execute(query)
        data = c.fetchone()
        return render_template('edit.html', row=data)

    except Exception:
        db.rollback()
        return "failed to update"

# --------------------------edit--------------------------------------------


# --------------------------Update--------------------------------------------

@app.route('/edit/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':

        Name = request.form['Name']
        Address = request.form['Address']
        Mobile = request.form['Mobile']
        Balance = request.form['Balance']
        # Photo = request.form['Photo']
        rid = request.form['Account']

        servername = "localhost"
        username = "root"
        password = ""
        dbname = "superhero_bank"

        try:

            db = pymysql.connect(servername, username, password, dbname)
            c = db.cursor()
            query = "update customer set Name='{}', Address='{}',Mobile='{}', Balance='{}' where Account='{}' ".format(Name, Address, Mobile, Balance, rid)
            c.execute(query)
            db.commit()
            return redirect(url_for('home'))

        except Exception:
            db.rollback()
            return "Failed to update"

# --------------------------Update--------------------------------------------

app.run(debug=True)