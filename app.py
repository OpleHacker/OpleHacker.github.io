# (A) INIT
# (A1) LOAD MODULES
from flask import Flask, render_template, request, make_response,flash,jsonify,url_for,redirect
import sqlite3

HOST_NAME = "localhost"
HOST_PORT = 81
DBFILE = "FIRST_AIDS.db"
app = Flask(__name__)
conn = sqlite3.connect(DBFILE)


# (B) HELPER FUNCTION - SEARCH USERS
def getusers(prs_no):
  prs_no = request.form.get("prs_no")
  prs_br = request.form.get("prs_br")
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM  View_all_employee WHERE PRS_NO =? AND PRS_BR=?  """,(prs_no,prs_br,))
  employee = cursor.fetchall()
  conn.close()
  return employee

def getdrug(name_search_drug):

  return name_search_drug




@app.route("/login", methods=["GET","POST"])
def login():
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute("SELECT Bu_ID,Bu_Name from tb_bu ")
  bu_user = cursor.fetchall()
  conn.close()
  return render_template("login.html",bu_user=bu_user)
    
@app.route("/", methods=["GET","POST"])
def index():
    # step 1 ค้นหาข้อมูลพนักงานด้วยรหัสพนักงานของแต่ละ BU.
  prs_br = request.form.get("prs_br")
  if request.method == "POST":
    data = dict(request.form)
    employee = getusers(data["prs_no"])
  else:
    employee = []

    
    
    # step 2  ค้นหาข้อมูลกลุ่มโรค
  conn2 = sqlite3.connect(DBFILE)
  cursor2 = conn2.cursor()
  cursor2.execute("SELECT id,desease_system,status,BU FROM desease_system WHERE status ='A'")
  #numrows = int(cursor.rowcount)
  desease_system = cursor2.fetchall()
  conn2.close()
  if desease_system == 0:
     flash("data does not exist!")
  # step 3  ค้นหาข้อมูลยาของแต่ละ BU.
  conn3 = sqlite3.connect(DBFILE)
  cursor3 = conn3.cursor()   
  cursor3.execute("SELECT id,item_code,item_name,description,medicin_bu FROM medicin WHERE status ='A' AND medicin_bu =?",[prs_br])
  numrows = int(cursor3.rowcount)
  medicines = cursor3.fetchall()
  conn3.close()
  if medicines == 0:
     flash("data does not exist!")
  return render_template("index.html", employee=employee,desease_system=desease_system,medicines=medicines,numrows=numrows)

@app.route("/select_drug/<id_drug>/<medicin_bu>", methods=["GET","POST"])
def select_drug(id_drug,medicin_bu):
    
    prs_id= request.form[('prs_id')]
    prs_no= request.form[('prs_no')]
    prs_br= request.form[('prs_br')]
    id_drug = id_drug
    com_deseas= request.form[('com_deseas')]
    with sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO 'reserv_drug' (emp_code,bu,item_code_drug,item_name_drug,id_drug) VALUES (?, ?, ?, ?, ?)", 
        (prs_id,prs_no,com_deseas,prs_br,id_drug))
        conn.commit()
    
    
    id_drug=id_drug
    cur.execute("SELECT * FROM reserv_drug ")
    reserv = cur.fetchall()
    print(medicin_bu)
   
    conn.close()


    return render_template('record.html',reserv=reserv)




@app.route("/search_drug",methods=["POST","GET"])
def search_drug():  
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    if request.method == 'POST':
       search_word = request.form['query']
       #print(search_word)
       if search_word == '':
           querys = "SELECT * FROM medicin ORDER BY id "
           cursor.execute(querys)
           medicins = cursor.fetchall()
           numrows = int(cursor.rowcount)
           print(numrows)
       else: 
           querys = "SELECT id,item_code,item_name,description,unit,type,pack1,pack2,medicin_bu,status FROM medicin WHERE item_code LIKE '%{}%' OR item_name LIKE '%{}%' OR description LIKE '%{}%' ORDER BY item_name ".format(search_word,search_word,search_word)
           cursor.execute(querys)
           print("Rows returned = ",cursor.rowcount)
           numrows = int(cursor.rowcount)
           medicins = cursor.fetchall()
    return medicins     
    #return jsonify({'htmlresponse': render_template('response_drug.html', medicins=medicins, numrows=numrows)})    

@app.route('/select_emp/<id>/<prs_br>', methods=['POST', 'GET'])
def select_emp(id,prs_br):
  conn1 = sqlite3.connect(DBFILE)
  cursor1 = conn1.cursor()
  cursor1.execute("SELECT * from View_all_employee where EMP_KEY=?", [id])
  employee = cursor1.fetchone()
  conn1.close()
  if employee == 0:
     flash("data does not exist!")

  conn2 = sqlite3.connect(DBFILE)
  cursor2 = conn2.cursor()
  cursor2.execute("SELECT * from desease_system  WHERE status ='A' AND bu  =? order by id",[prs_br])
  numrows = int(cursor2.rowcount)
  desease_system = cursor2.fetchall()
  conn2.close()
  if desease_system == 0:
     flash("data does not exist!")
  
  conn3 = sqlite3.connect(DBFILE)
  cursor3 = conn3.cursor()   
  cursor3.execute("SELECT id,item_code,item_name,description FROM medicin WHERE status ='A' AND medicin_bu =?",[prs_br])
  numrows = int(cursor3.rowcount)
  medicines = cursor3.fetchall()
  conn3.close()
  if medicines == 0:
     flash("data does not exist!")
  return render_template("record.html", employee=employee,desease_system=desease_system,medicines=medicines,numrows=numrows)

@app.route('/init_db',methods = ['POST', 'GET']) 
def init_db():
    msg=''
    data = [{'title':'ajsdhkd', 'author': 'askjdh qweqwqw'}, {'title':'ajsdhkd', 'author': 'askjdh qweqwqw'}]

    conn = sqlite3.connect('FIRST_AIDS.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    #cursor.execute("CREATE TABLE 'books' (title TEXT, author TEXT);")    
    sql = "INSERT INTO 'books' (title, author) VALUES (?, ?);"
    #sql = "INSERT INTO reserv_drug (reserv_bu,id_drug,item_code_drug,item_name_drug) VALUES (?,?,?,?);"
    for book in data:
        cursor.execute(sql, (book['title'], book['author']))

    conn.commit()
    conn.close()
    return "Hello"
    #return render_template("record.html", )
   
    #return render_template('S3_users.html',msg = msg)
   
@app.route('/temp_record/<id_drug>',methods = ['POST', 'GET']) 
def temprecord(id_drug):
    prs_id= request.form[('prs_id')]
    prs_no= request.form[('prs_no')]
    prs_br= request.form[('prs_br')]
    id_drug = id_drug
    com_deseas= request.form[('com_deseas')]
    with sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO 'reserv_drug' (emp_code,bu,item_code_drug,item_name_drug,id_drug) VALUES (?, ?, ?, ?, ?)", 
        (prs_id,prs_no,com_deseas,prs_br,id_drug))
        conn.commit()
        #conn.close()
    return "Hello"
    #return redirect(url_for('index'))


    #return render_template("record.html", )
   
    #return render_template('S3_users.html',msg = msg) 
 # ************** start test************************** 




@app.route('/index',methods=['GET','POST'])
def addcomment():
    if request.method=="GET":
        return render_template('index.html')
    else:
        user_details=(
        request.form['title'],
        request.form['name'],
        request.form['comment']
            )
        print(user_details)
        insertcomment(user_details)
        return render_template('addsuccess.html')

#INSERTING comments into the actual database
def insertcomment(user_details):
        connie = sqlite3.connect('FIRST_AIDS.db')
        c=connie.cursor()
        sql_insert_string='INSERT INTO comments (title, name, comment) VALUES (?,?,?)';
        c.execute(sql_insert_string,user_details)
        connie.commit
        connie.close()
        print(user_details)


def query_comments():
        connie = sqlite3.connect('FIRST_AIDS.db')
        c=connie.cursor()
        c.execute("""
        SELECT * FROM comments  

        """)
        userdata=c.fetchall()
        return userdata    
 # ************** end test**************************   
@app.route('/test', methods=["POST", "GET"])
def transactions_view():
    time = (request.args.get("test"))
    return render_template("record.html", time=time)
  
 
    
     

def check():
    if request.method=='POST':
        Operations=request.form['Operations']
        
        if(Operations=="Run Pipeline"):

            return ('index.html', Operations)

        elif (Operations=="Check state and result of pipeline"):
            
            return ('index.html', Operations)
    else:
        return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)
