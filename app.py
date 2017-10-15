import MySQLdb
import dblib
from flask import Response
from flask import request
from flask import Flask
from flask import json
from json import dumps

app = Flask(__name__)

#db = MySQLdb.connect("localhost", "user", "passwd", "app_db")
#curs=db.cursor()

@app.route('/postdata', methods = ['POST'])

def postJsonData():

    if  request.headers['Content-type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-type'] == 'application/json':
	#connect to app_db
         conn=dblib.connectToSQLDatabase()          
         curs=conn.cursor() 	 

	#JSON Handle
         content = json.dumps(request.json)
         contentDictionary = json.loads(content)
         
	 vehicle_id=contentDictionary["v_id"]
	 route_id=contentDictionary["r_id"]
	 
         cool_temp=int(contentDictionary["cool_temp"])
	 maf_pressure=int(contentDictionary["maf_pre"])
         rpm=int(contentDictionary["rpm"])
         speed=int(contentDictionary["speed"])
         throttle=int(contentDictionary["thr"])
         latitute=float(contentDictionary["lat"])
	 longitute=float(contentDictionary["lon"])       
  
         try:
             curs.execute("""INSERT INTO MEASUREMENTS (ROUTE_ID,VEHICLE_ID,COOL_TEMP,MAF_PRESSURE,RPM,SPEED,THROTTLE,LAT,LON) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(route_id,vehicle_id,cool_temp,maf_pressure,rpm,speed,throttle,latitute,longitute))

             conn.commit()
             print "Data committed"


         except:
                print "Error: the database is being rolled back"
                conn.rollback()
                conn.close()
	
         conn.close()

         return "JSON Message:Post Data OK"

   
    else:
	return "415 Unsupported Media Type ;)"

@app.route('/livedata', methods = ['GET'])
def getData():
    conn=dblib.connectToSQLDatabase()
    query='select * from MEASUREMENTS ORDER BY MEASUREMENT_DATE_TIME DESC LIMIT 1' 
    rows=dblib.runQuery(conn,query)
    conn.close()
    rv={"r_id":rows[0][0],"v_id":rows[0][1],"date_time":str(rows[0][2]),"cool_temp":rows[0][3],"maf_pre":rows[0][4],"rpm":rows[0][5],"speed":rows[0][6],"thr":rows[0][7],"lat":rows[0][8],"lon":rows[0][9]}    
    Response.content_type = 'application/json'
    return dumps(rv)	

#if __name__ == "__main__":
#   app.run(host='0.0.0.0', port=80, debug=True)


