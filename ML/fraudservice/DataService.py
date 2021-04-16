
import MySQLdb

def dbconnect():
    try:
        db = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='password',
            db='Fraud'
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return db

def insertDb():
    try:
        db = dbconnect()
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO Results(FraudResult) \
        VALUES (%s) """, (data))
        cursor.close()
    except Exception as e:
        print e