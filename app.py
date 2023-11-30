from flask import Flask, render_template, request, make_response,jsonify, flash, redirect, request, url_for, session
from flaskext.mysql import MySQL
import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
import numpy as np
from datetime import datetime
import time
import mysql.connector
import datetime
import os



app = Flask(__name__)
app.secret_key = b'\x0f\xcf\xf0w\xdc\x93f\xd7\xa8\xffs^'

mysql = MySQL(autocommit = True, cursorclass = pymysql.cursors.DictCursor)
mysql.init_app(app)

# configuring MySQL for the web application
app.config['MYSQL_DATABASE_USER'] = 'root'   
app.config['MYSQL_DATABASE_PASSWORD'] = 'password' 
app.config['MYSQL_DATABASE_DB'] = 'med'  
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 


#initialise mySQL
#create connection to access data
conn = mysql.connect()
cursor = conn.cursor()


@app.route('/AddStock', methods=['GET', 'POST'])
def AddStock():
    if request.method == 'POST':
        # Get form data
        pid = request.form['pid']
        pname = request.form['pname']
        supplier = request.form['supplier']
        price = request.form['price']
        quantity= request.form['quantity']
        expire=request.form['expire']

        query= "Insert into medicine values(%s,%s,%s,%s,%s,%s)"
        values=(pid,pname,supplier,price,quantity,expire)
        cursor.execute(query,values)
        # query = "SELECT * FROM LoginPatient where enroll = '" + enroll+ "' and pass = '" + password+ "'"


        print(query)
        result = cursor.fetchall()
        print(result)

        # If login credentials are correct, redirect to home page
        # if result:
        #     session["loggedin"] = True
        #     session["enroll"]= enroll
        #     return redirect(url_for('home'))

        # # If login credentials are incorrect, show error message
        # else:
        #     error = 'Invalid email or password. Please try again.'
            # return render_template('LoginPatient.html', error=error)

    return render_template('basic_elements.html')

@app.route('/')
@app.route('/home')
def home():
    # check if user is logged in or not
    # if 'loggedin' in session:
    #     user_is_logged_in = True
    # else:
    #     user_is_logged_in = False
    return render_template('index.html')

@app.route('/inventory' ,methods=['GET', 'POST'])
def inventory():

    query = "SELECT * FROM medicine"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)

    updated_result = []
    for record in result:
        expiry_date = record['expiry']  # Assuming expiry date is in 6th column (index 5)
        today = datetime.datetime.now().date()
        days_until_expiry = (expiry_date - today).days
        
        record['days_until_expiry'] = days_until_expiry

        # updated_record = record + (days_until_expiry,)  # Adding days until expiry to the record tuple
        updated_result.append(record)

    # return updated_result
    print(updated_result)

    return render_template('basic-table.html',updated_result=updated_result)






# @app.route('/request' , methods=['GET','POST'])
# def requests():
#     # check if user is logged in or not
#     if 'loggedin' in session:
#         if 'enroll' in session:
#             if request.method == 'POST':
#                 # return render_template('request.html')
#             #Get Form data
#                 enrollment = session['enroll']
#                 query1 = "select Pname from Students where enroll =%s"
#                 val= (enrollment,)
#                 cursor.execute(query1,val)
#                 nameEnroll = cursor.fetchone()
#                 name= nameEnroll["Pname"]
#                 number=request.form['number']
#                 enroll= session['enroll']
#                 gender= request.form['gender']
#                 age= request.form['age']
#                 requirement= request.form['requirement']
#                 medname= request.form['medname']
#                 symptoms=request.form['symptoms']
#                 prescription=request.files['prescription']  #prescription or filename
#                 file = prescription.filename
#                 prescription.save(os.path.join("./uploads", file))
#                 status = "Approval Pending" #approval pending, approved, completed
#                 date = datetime.datetime.now()

#                 query= "Insert into requests values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 values=(name,number,enroll,gender,age,requirement,medname,symptoms,file,date,status)
#                 cursor.execute(query,values)

#                 return redirect(url_for('home'))
            
#             enrollment = session['enroll']
#             query1 = "select Pname,enroll from Students where enroll =%s"
#             val= (enrollment,)
#             cursor.execute(query1,val)
#             nameEnroll = cursor.fetchone()
#             print(nameEnroll)
#             return render_template('request.html', nameEnroll= nameEnroll )
            
#     else:
#         return redirect(url_for('LoginPatient'))
    
#     return render_template('request.html')

        #session['name']= fetch from mysql
    # if 'user_id' in session:
        # Connect to the MySQL database
    #     cnx = mysql.connector.connect(**db_config)
    #     cursor = cnx.cursor()

    #     # Fetch data from the MySQL table based on the session variable value
    #     query = "SELECT * FROM your_table_name WHERE user_id = %s"
    #     cursor.execute(query, (session['user_id'],))
    #     data = cursor.fetchall()

    #     # Close the MySQL database connection
    #     cursor.close()
    #     cnx.close()

    #     # Pass the data to the HTML template for rendering
    #     return render_template('data.html', data=data)
    # else:
    #     # Redirect to the login page if the session variable is not set
    #     return redirect('/login')

# @app.route('/dashboard' , methods=['GET','POST'])
# def dashboard():
# # check if user is logged in or not
#     if 'loggedin' in session:
#         if 'enroll' in session:
#             enrollment=session['enroll']
#             query = "select Pname from Students where enroll=%s"
#             values = (enrollment,)
#             cursor.execute(query,values)
#             result = cursor.fetchone()
#             query1= "select medname,req_status,date_time from requests where enroll= %s order by req_status"
#             values1= (enrollment,)
#             cursor.execute(query1,values1)
#             result1= cursor.fetchall()
#             query2 = "SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(symptoms, ' ', n.n), ' ', -1)) AS common_word, COUNT(*) AS count FROM prescriptions CROSS JOIN (SELECT a.N + b.N * 10 + 1 n FROM (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a JOIN (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b ORDER BY n ) n WHERE n.n <= 1 + (LENGTH(symptoms) - LENGTH(REPLACE(symptoms, ' ', ''))) AND enroll = %s GROUP BY common_word ORDER BY count desc;"
#             values2= (enrollment,)
#             cursor.execute(query2,values2)
#             result2= cursor.fetchall()
#             query3= "select count(*) as count_ from prescriptions where enroll=%s;"
#             values3= (enrollment,)
#             cursor.execute(query3,values3)
#             res= cursor.fetchone() 
#             count= res["count_"]
#             return render_template('dashboard.html',result=result, result1= result1,result2=result2,count=count)
#         elif 'DocID' in session:
#             return render_template('dashboard1.html')
#     else:
#         return redirect(url_for('LoginPatient'))
    # return render_template('dashboard.html')



    



# Replace 'your_table' and 'expiry_date_column' with your actual table and column names






if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
