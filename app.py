from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from email_send import email_send

app=Flask(__name__)

env='prod'
if env=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/f_form'

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nycberwonqlmvw:ab8c4d80eb8f15cf61cdb3687f6c2a05d089445b49053073a388774f7a6a11da@ec2-3-216-89-250.compute-1.amazonaws.com:5432/der592qr6q8kjd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app) #create database object

class feedback(db.Model):  # create models to query
    _tablename_='feedback'
    id=db.Column(db.Integer,primary_key=True)
    customer=db.Column(db.String(300),unique=True)
    platform= db.Column(db.String(300))
    product = db.Column(db.String(300))
    ease_of_use=db.Column(db.Integer)
    delivery=db.Column(db.Integer)
    quality=db.Column(db.String(200))
    refer=db.Column(db.Integer)
    comments=db.Column(db.Text())

    def __init__(self,customer,platform,product,ease_of_use,delivery,quality,refer,comments):
        self.customer=customer
        self.platform=platform
        self.product=product
        self.ease_of_use=ease_of_use
        self.delivery=delivery
        self.quality=quality
        self.refer=refer
        self.comments=comments



@app.route("/",methods=["POST","GET"])

def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method=="POST":
        customer=request.form['customer']
        Platform=request.form["Platform"]
        product=request.form["product"]
        ease=request.form["rating"]
        delivery=request.form["rating1"]
        quality=request.form["quality"]
        refer=request.form["rating2"]
        comments=request.form["comments"]
        #print(customer,Platform,product,ease,delivery,quality,refer,comments)
        if customer=='' or Platform=='':
            return render_template("index.html", message="Please enter the required fields")
        if db.session.query(feedback).filter(feedback.customer==customer).count()==0:
            data=feedback(customer,Platform,product,ease,delivery,quality,refer,comments)
            db.session.add(data)
            db.session.commit()
            email_send(customer,Platform,product,ease,quality,delivery,refer,comments)
            return render_template('submitted.html')
        return render_template("index.html", message="You have already submitted a feedback")


if __name__=="__main__":
    app.run(port=8000)