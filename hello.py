from flask import Flask, render_template,request
import os
import ibm_db

app = Flask(__name__)

#port = int(os.getenv("VCAP_APP_PORT")) # cloud app
port = os.getenv("VCAP_APP_PORT") # locally run app
conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=pbj53543;PWD=47g0@xwjcz8f70hc;","","")
#conn = mysql.connector.connect(host='localhost', database='BindhuDB',user='root',password='BinMay18!')

@app.route('/')
def index():
    query = "SELECT * FROM data"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.execute(stmt)
    rows = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(stmt)
    # ibm_db.close(conn)
    return render_template('home.html', data=rows)

#######################  Display Image when name is given  ############################
@app.route('/findRoom', methods=['GET', 'POST'])
def imagename():
    if request.method == 'POST':
        name = request.form['name']
        query4 = 'SELECT * FROM data where "name" = \'' + name + '\' '
        print(query4)
        stmt4 = ibm_db.prepare(conn, query4)
        ibm_db.execute(stmt4)
        rows = []

        result4 = ibm_db.fetch_assoc(stmt4)
        while result4 != False :
            rows.append(result4.copy())
            result4=ibm_db.fetch_assoc(stmt4)

    return render_template("findRoom.html", data = rows)


#######################  Display Image when salaray is less than the given input ############################
@app.route('/salaryLessThan', methods=['GET', 'POST'])
def imagesalary():
    if request.method == 'POST':
        salary = request.form['salary']
        query4 = 'SELECT * FROM data where "salary" < \'' + salary + '\' '
        print(query4)
        stmt4 = ibm_db.prepare(conn, query4)
        ibm_db.execute(stmt4)
        rows = []

        result4 = ibm_db.fetch_assoc(stmt4)
        while result4 != False :
            rows.append(result4.copy())
            result4=ibm_db.fetch_assoc(stmt4)

    return render_template("salaryLessThan.html", data = rows)


#######################  Adding images ############################
@app.route('/addPicture', methods=['GET', 'POST'])
def addimage():
    if request.method == 'POST':
        picture = request.form['picture']
        upname = request.form['upname']
        query4 = 'UPDATE data SET  "picture" = \'' + picture + '\' where "name" = \'' + upname + '\' '
        print(query4)
        stmt4 = ibm_db.prepare(conn, query4)
        ibm_db.execute(stmt4)
        query = "SELECT * FROM data"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        rows = []
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

    return render_template("addPicture.html", data = rows)


#######################  Removing record ############################
@app.route('/removeRecord', methods=['GET', 'POST'])
def removeperson():
    if request.method == 'POST':
        upname = request.form['upname']
        query4 = 'DELETE FROM data where "name" = \'' + upname + '\' '
        print(query4)
        stmt4 = ibm_db.prepare(conn, query4)
        ibm_db.execute(stmt4)
        query = "SELECT * FROM data"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        rows = []
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

    return render_template("removeRecord.html", data = rows)


#######################  Changing keywords ############################
@app.route('/updateKeywords', methods=['GET', 'POST'])
def upkeywords():
    if request.method == 'POST':
        nameup = request.form['upname1']
        key = request.form['upkey']
        # print(key)
        query5 = 'UPDATE data SET "keywords" = \''+key+'\' where "name" = \''+nameup+'\' '
        print(query5)
        stmt5 = ibm_db.prepare(conn, query5)
        ibm_db.execute(stmt5)
        query = "SELECT * FROM data"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        rows = []
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

    return render_template("updateKeyword.html", data=rows)


#######################  Changing salary ############################
@app.route('/changeSalary', methods=['GET', 'POST'])
def upsalary():
    if request.method == 'POST':
        nameup = request.form['upname']
        salary = request.form['salary']
        # print(key)
        query5 = 'UPDATE data SET "salary" = \''+salary+'\' where "name" = \''+nameup+'\' '
        print(query5)
        stmt5 = ibm_db.prepare(conn, query5)
        ibm_db.execute(stmt5)
        query = "SELECT * FROM data"
        stmt = ibm_db.prepare(conn, query)
        ibm_db.execute(stmt)
        rows = []
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)

    return render_template("changeSalary.html", data=rows)

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return render_template('500.html',title='500')

    
if __name__ == '__main__':
    #app.run(host='127.0.0.1', port= 8080, debug=True) # Local
    app.run(host='0.0.0.0', port=port, debug=True) # Cloud
