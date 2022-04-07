from flask import Flask , render_template , request
import sqlite3 as sql

from werkzeug.utils import redirect

connection = sql.connect("Hospital.db",check_same_thread=False)
listofpatient = connection.execute("select name from sqlite_master where type='table' AND name='patient'").fetchall()

if listofpatient!=[]:
    print("Table exist already")
else:
    connection.execute('''create table patient(
                                ID integer primary key autoincrement,
                                name text,
                                mobnumber integer,
                                age integer,
                                address text,
                                dob text,
                                place text,
                                pincode integer                                                         
                                );''')
    print("Table Created Successfully")

hospital = Flask(__name__)

@hospital.route("/",methods = ["GET","POST"])
def admin_login():
    if request.method == "POST":
        getusername=request.form["username"]
        getpassword=request.form["password"]
        print(getusername)
        print(getpassword)
        if getusername == "admin" and getpassword=="12345":
            return redirect("/dashboard")
    return render_template("admin.html")

@hospital.route("/dashboard",methods = ["GET","POST"])
def patient_registration():
    if request.method == "POST":
        getname = request.form["name"]
        getmobnumber = request.form["mobnumber"]
        getage = request.form["age"]
        getaddress = request.form["address"]
        getdob = request.form["dob"]
        getplace = request.form["place"]
        getpincode = request.form["pincode"]
        print(getname)
        print(getmobnumber)
        print(getage)
        print(getaddress)
        print(getdob)
        print(getplace)
        print(getpincode)

        try:
            connection.execute("insert into patient(name,mobnumber,age,address,dob,place,pincode)\
                               values('" + getname + "'," + getmobnumber + "," + getage + ",'" + getaddress + "','" + getdob + "','" + getplace + "'," + getpincode + ")")
            connection.commit()
            print("Student Data Added Successfully")
            return redirect("/viewall")
        except Exception as error:
            print("Error occured ", error)

    return render_template("dashboard.html")

@hospital.route("/viewall")
def view_patient():
    cursor = connection.cursor()
    cursor.execute("select * from patient")
    result = cursor.fetchall()
    return render_template("viewall.html",patient=result)

@hospital.route("/search",methods = ["GET","POST"])
def search_patient():
    cursor = connection.cursor()
    if request.method == "POST":
        getmobnumber = request.form["mobnumber"]
        cursor.execute("select * from patient where mobnumber ="+getmobnumber+" ")
        result = cursor.fetchall()
        if result is None:
            print("mob num not exists ")
        else:
            return render_template("search.html",search=result,status=True)
    else:
        return render_template("search.html", search=[], status=False)

@hospital.route("/delete",methods = ["GET","POST"])
def delete_patient():
    if request.method == "POST":
        getmobnumber = request.form["mobnumber"]
        print(getmobnumber)
        connection.execute("delete from patient where mobnumber="+getmobnumber)
        connection.commit()
        print("Patient data Deleted Successfully.")
        return redirect('/viewall')

    return render_template("delete.html")

@hospital.route('/up', methods=['GET', 'POST'])
def update():
    global mobnumber
    connection.cursor()
    if request.method == "POST":
        mobnumber = request.form["mobnumber"]
        return redirect('/update')

    return render_template("update.html")

@hospital.route("/update",methods = ["GET","POST"])
def update_patient():
    if request.method == "POST":
        mobnumber = request.form["mobnumber"]
        name = request.form["name"]
        age = request.form["age"]
        address = request.form["address"]
        dob = request.form["dob"]
        place = request.form["place"]
        pincode = request.form["pincode"]
        connection.execute("update patient set name='" + name + "',age=" + age + ",address='" + address + "',dob='" + dob + "',place='" + place + "',pincode=" + pincode + " where mobnumber=" + mobnumber)
        connection.commit()
        print("Updated Successfully")

        return redirect('/viewall')

    return render_template("updatation.html")


if __name__ == "__main__":
    hospital.run()