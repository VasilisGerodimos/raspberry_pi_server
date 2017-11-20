import MySQLdb


hostname = 'localhost'
database = 'app_db'
username='root'
password=''

def connectToSQLDatabase():
       #print 'Using MySQL - library'
	conn = MySQLdb.connect(host='localhost', user='user', passwd='passwodd', db='app_db')
	print 'Connected to MySQL'
	return conn

def runQuery(conn, query):
	rows = ""
	try:
		cur = conn.cursor()
		cur.execute("USE %s;" % database)
		cur.execute(query)
		#Important to commit the data
		conn.commit()
		rows = cur.fetchall()
		#for row in rows:
	                #print row
	except:
		conn.rollback()
		print "Something went wrong. Rollback to previous state"
        
        return rows
