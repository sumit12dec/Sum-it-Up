
from flask import Flask, render_template, request, jsonify
import summarize
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/Add", methods=["GET","POST"])
def add():
	a = request.form.get("value_a")
	if "http" not in a:
		a="http://"+a
	#sum1=int(a)+int(b)
        sum1 =summarize.main1(a)
	return render_template("Add.html", a=a,sum1=sum1)


def db_connect(passed_url):
	import MySQLdb	
	db = MySQLdb.connect("localhost","root","root","beta")
    	cursor = db.cursor()
	sql = """select * from sumup where id='%s'""" % (passed_url)
	print sql,"db_connect"
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Fetch all the rows in a list of lists.
	   results = cursor.fetchall()
	   # print results,"1111111111111111111"
	   url = results[0][0]
	   summary = results[0][1]
	   # Now print fetched result
	   print " Summary Exists...Retrieving from DB"
	   return list((url, summary))
	except:
	   print "Error: unable to fetch data"
	db.commit()
	db.close()


@app.route("/API", methods=["GET","POST"])
def api_call():
	
	passed_url = request.args.get('url')
	values = db_connect(passed_url)
	if values!=None:
		return values[1]
	else:
		print "Doesn't exists in DB...scraping and then summarizing"
		if "http" not in passed_url:
			passed_url="http://"+passed_url
		#sum1=int(a)+int(b)
        	sum1 =summarize.main1(passed_url)
		import MySQLdb	
		db = MySQLdb.connect("localhost","root","root","beta")
	    	cur = db.cursor()
		sql = """insert into sumup values('%s', "%s")"""%(passed_url, sum1)
		#print sql,"000"
		try:
		   cur.execute(sql)
		   logging.warning("writing in DB")
		except:
		   print "Error: unable to write the data"
		db.commit()
		db.close()
		return sum1

if __name__ == "__main__":
	app.run(debug=True)
