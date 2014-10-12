#appcfg.py -A enduring-grid-600 update appengine-try-python
from flask import Flask, render_template, request, jsonify
import summarize
import summ
app = Flask(__name__)

# main index
@app.route("/")
def index():
	return render_template("index.html")

# cobrand session token
@app.route("/Add", methods=["GET","POST"])
def add():
	a = request.form.get("value_a")
	if "http" not in a:
		a="http://"+a
	#sum1=int(a)+int(b)
        sum1 =summarize.main1(a)
	return render_template("Add.html", a=a,sum1=sum1)


@app.route("/API", methods=["GET","POST"])
def api_call():
	passed_url = request.args.get('url')
	if "http" not in passed_url:
		passed_url="http://"+passed_url
	#Algorithm based on sentence score with the count of important words
        #sum1 =summarize.main1(passed_url)
	#algorithm based on word in title
        sum2 = summ.sum2(passed_url)
	return sum2

if __name__ == "__main__":
	app.run(debug=True)
