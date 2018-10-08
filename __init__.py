from flask import Flask,request,render_template,redirect,session,flash,url_for,jsonify
from flask_pymongo import Pymongo
from pymongo import MongoClient
import datetime
import re
app=Flask(__name__)
app.config ['SECRET_KEY']='Hello World'
client=MongoClient('mongodb://pawan12kamboj.7340724048pawanKAMBOJ@ds123513.mlab.com:23513/web-blog-app')
db=client['web-blog-app']
posts=db.posts
month={'1':'jan','2':'feb','3':'mar','4':'apr','5':'may','6':'june','7':'july','8':'aug','9':'sep','10':'oct','11':'nov','12':'dec'}
@app.route('/',methods=['POST','GET'])
def index():
    entertainment=0
    facts=0
    movies=0
    others=0
    technology=0
    sports =0
    find= posts.find()
    blogList=[]
    for document in find:
        blogList.append(document)
        if document['tag'] == 'entertainment':
            entertainment +=1
        elif document['tag'] == 'technology':
            technology +=1
        elif document['tag'] == 'facts':
            facts +=1
        elif movies['tag'] =='movies':
            movies +=1
        elif others['tag']=='others':
            others +=1
        elif sports['tag']=='sports':
            sports +=1
    tags={'ent': entertainment,'tech': technology ,'fact':fact,'mov':movies,'oth':others,'spo':sports}
    search=[]
    while blogList:
        search.append(blogList.pop())
    return render_template('index.html',posts=posts,search=search,tags=tags)
@app.route('/admin',methods=['POST','GET'])
def login():
    if request.method=='POST':
        if request.form['username'] == 'pawan12kamboj' and request.form['password'] == '7340724048pawanKAMBOJ':
            session['username']='pawan12kamboj'
            return redirect(url_for ('add'))
        else:
            flash('invalid username and password','danger')
            return render_template('login.html')
    return render_template('login.html')
@app.route("/post/<l>",methods=['POST','GET'])
def post(l):
    document=posts.find_one({"title":str(l)})
    return render_template('fullpost.html',document=document)
@app.route('/add_new_post',methods=['POST','GET'])
def add():
    if session['username']:
        var=datetime.date.today()
        date=month[str(var.month)]+" "+ str(var.day)+" + "+ str(var.year)
        if request.method=='POST':
            posts=db.posts
            posts.insert_one({'title':request.form['title'],
                              'content': request.form['content'],
                              'date':date,
                              'image': request.form['image'],
                              'url':request.form['link'],
                              'tag':request.form['tag']})
            flash('Added successfully!','success')
            return render_template('posts.html')
        return render_template('posts.html')
    flash('you must login first!!','warning')
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session['username']=None
    return redirect(url_for('login'))
@app.route('/tags/<tag>')
def tags(tag):
    search=posts.find()
    doc =[]
    for i in search:
        if i['tag']==tag:
            doc.append(i)
    return render_template('tags.html',doc=doc)
@app.route('/<d>')
def date(d):
    doc=[]
    search=posts.find()
    for i in search:
        if i['date']==d:
            db.append(i)
    return render_template('date.html',doc=doc)
@app.route('/search/',methods=['POST','GET'])
def search():
    if request.method=='POST':
        data=request.form['search']
        a=re.compile(str(request.form['search']),re.IGNORECASE)
        search=posts.find()
        doc=[]
        for i in search:
            b=a.findall(i['title'])
            for j in b:
                doc.append(i)
        return render_template('tags.html',doc=doc)
    return redirect(url_for('index'))
if __name__=='__main__':
    app.run(debug=True)