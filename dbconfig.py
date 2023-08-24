import mysql.connector
from mysql.connector import errors
from rich import print as printc
from cryptoGraphy import cryptoGraphy
def connectDB():
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root"
        ) 
    except Exception as e:
        printc(f"[red]{e}[/red]")
    return mydb

def createDB():
    mydb = connectDB()
    mycursor = mydb.cursor()
    comList = ["CREATE DATABASE userpass",
               "USE userpass",
               "CREATE TABLE userlist(user VARCHAR(225), password VARCHAR(225), cryptographyKey VARCHAR(225), PRIMARY KEY (user))",
               "CREATE TABLE passlist(user VARCHAR(225),webName VARCHAR(225) NOT NULL, url VARCHAR(225) NOT NULL, mail VARCHAR(225) NOT NULL, id VARCHAR(225) NOT NULL, password VARCHAR(225) NOT NULL, note VARCHAR(225), FOREIGN KEY (user) REFERENCES userlist(user))" 
               ]
    for query in comList:
        try:
            mycursor.execute(query)
            status = True
        except errors.DatabaseError as e:
            if e.errno == 1007:
                printc("[yellow][!] Database already exits.[/yellow]")
            status = "None"
    if status is True:
        printc("[green][+] Installation completed. You're ready to use APM![/green]")
    elif status == "None":
        pass
    else:
        printc("[red] [x]Installation failed.[/red]")
    mydb.close()
    
def dropDB():
    mydb = connectDB()
    mycursor = mydb.cursor()
    comList = ["DROP DATABASE userpass"]
    for query in comList:
        try:
            mycursor.execute(query)
            printc("[green][ 🗸] Database deleted successfully.[/green]")
        except Exception as e:
            printc(f"[red]{e}[/red]")
    mydb.close()
class updateDB:
    def update(self, user, password, key):
        mydb = connectDB()
        mycursor = mydb.cursor()
        sql = "INSERT INTO userlist (user, password, cryptographyKey) VALUES (%s, %s, %s)"
        val = (user, password, key)
        try:
            mycursor.execute("USE userpass")
            mycursor.execute(sql, val)
        except Exception as e:
            printc(f"[red]{e}[/red]")
        mydb.commit()
        mydb.close()
    
    def checkUser(self, user):
        mydb = connectDB()
        mycursor = mydb.cursor()
        try:
            mycursor.execute("USE userpass")
            query = "SELECT * FROM userlist WHERE user = %s"
            mycursor.execute(query,(user,))
            result = mycursor.fetchone()
            if result:
                printc("[red][x] Username already exits. Try again...[/red]")
            else:
                return True
        except Exception as e:
            printc(f"[red]{e}[/red]")
        mydb.close()

    def userAuth(self, user, password):
        mydb = connectDB()
        mycursor = mydb.cursor()
        try:
            mycursor.execute("USE userpass")
            query = "SELECT * FROM userlist WHERE user = %s"
            mycursor.execute(query, (user, password))
            userDB, passwordDB, cryptograhyKeyDB = mycursor.fetchone()
            decryptedPass = cryptoGraphy.decrypt(cryptograhyKeyDB, passwordDB)
            if password == decryptedPass:
                return True
            else:
                printc("[red][x]Access denied.[/red]")
                return False
        except Exception as e:
            printc(f"[red]{e}[/red]")
        mydb.close()

    def DBCheck(self):
        mydb = connectDB()
        mycursor = mydb.cursor()
        status = None
        try:
            mycursor.execute("USE userpass")
            status = True
        except errors.DatabaseError as e:
            if e.errno == 1049 :
                status = False
        return status
        mydb.close()


    def userDataCheck(self):
        mydb = connectDB()
        mycursor = mydb.cursor()
        try:
            mycursor.execute("USE userpass")
            mycursor.execute("SELECT * FROM userlist")
            result = mycursor.fetchone()
            if result:
                return True
            else:
                return "None"
        except errors.DatabaseError as e:
            if e.errno == 1049:
                return "NoDB"
        mydb.close()