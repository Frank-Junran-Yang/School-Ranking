from os import readlink, stat
from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
from flask_sqlalchemy import SQLAlchemy
from utils import listToString, capital, char, digit

app = Flask(__name__)
app.secret_key = 'dfghjiouhgyfvhbjaknsdasidnasiodn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///School.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    username = db.Column(db.String(80),unique=True, nullable=True)
    password=db.Column(db.String(80), nullable=True)
    firstname=db.Column(db.String(80), nullable=True)
    lastname=db.Column(db.String(80), nullable=True)
    money=db.Column(db.Integer, nullable=True)
    favorite=db.Column(db.String(1000),unique=True)

class PrivateSchools(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(80),unique=True, nullable=True)
    location=db.Column(db.String(80), nullable=True)
    tuitionfee=db.Column(db.Integer, nullable=True)
    size=db.Column(db.String(80), nullable=True)
    matriculation=db.Column(db.String(100), nullable=True)
    rank = db.Column(db.Integer, nullable=True)
    @staticmethod
    def includes(name):
        privates=PrivateSchools.query.filter_by(name = name).all()
        if (privates):
            return True
        return False

class PublicSchools(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(80),unique=True, nullable=True)
    location=db.Column(db.String(80), nullable=True)
    tuitionfee=db.Column(db.Integer, nullable=True)
    size=db.Column(db.String(80), nullable=True)
    matriculation=db.Column(db.String(100), nullable=True)
    rank = db.Column(db.Integer, nullable=True)
    @staticmethod
    def includes(name):
        publics=PublicSchools.query.filter_by(name = name).all()
        if (publics):
            return True
        return False

class BoardingSchools(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(80),unique=True, nullable=True)
    location=db.Column(db.String(80), nullable=True)
    tuitionfee=db.Column(db.Integer, nullable=True)
    size=db.Column(db.String(80), nullable=True)
    matriculation=db.Column(db.String(100), nullable=True)
    rank = db.Column(db.Integer, nullable=True)

    @staticmethod
    def includes(name):
        boardings=BoardingSchools.query.filter_by(name = name).all()
        if (boardings):
            print(boardings)
            return True
        return False

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.jinja'), 404


@app.route('/',methods=['POST','GET'])
def index():
    privates= PrivateSchools.query.all()
    publics= PublicSchools.query.all()
    boardings= BoardingSchools.query.all()
    prilen=len(privates)
    publen=len(publics)
    boalen=len(boardings)
    return render_template('index.jinja',privates=privates,publics=publics,boardings=boardings, prilen=prilen, publen=publen, boalen=boalen)

@app.route('/register',methods=['POST','GET'])
def register():
    warning=''
    success=''
    try:
        if (request.method == 'POST'):
            username=request.form.get('username')
            password = request.form.get('password')
            check=request.form.get('check')
            firstname=request.form.get('firstname')
            lastname=request.form.get('lastname')
            if password!=check:
                warning='Password Does Not Match!!!'
                return render_template('register.jinja',warning=warning)

            
            if password==check:
                if len(password)<=6:
                    warning='Your password is too short, please make it longer than 6 characters'
                    return render_template('register.jinja',warning=warning)
                elif len(password)>=20:
                    warning='Your password is too long, please make it no longer than 20 characters'
                    return render_template('register.jinja',warning=warning)
                elif not capital(password):
                    warning='You need to have at least one digit, one capital letter, and one letter'
                    return render_template('register.jinja',warning=warning)
                elif not digit(password):
                    warning='You need to have at least one digit, one capital letter, and one letter'
                    return render_template('register.jinja',warning=warning)
                elif not char(password):
                    warning='You need to have at least one digit, one capital letter, and one letter'
                    return render_template('register.jinja',warning=warning)
                user=User(username=username, password=password, firstname=firstname, lastname=lastname, money=1000)
                db.session.add(user)
                db.session.commit()
                success='Register Successfully'
                return redirect(url_for('login'))
    except:
        return redirect(url_for('register'))
    return render_template('register.jinja',warning=warning,success=success)

@app.route('/registerprivate',methods=['POST','GET'])
def registerprivate():
    try:
        if (request.method == 'POST'):
            name=request.form.get('name')
            location = request.form.get('location')
            tuitionfee=request.form.get('tuitionfee')
            size=request.form.get('size')
            matriculation=request.form.get('matriculation')
            rank=request.form.get('rank')
            
            private=PrivateSchools(name=name, location=location, tuitionfee=int(tuitionfee), size=size, matriculation=matriculation, rank=int(rank))
            db.session.add(private)
            db.session.commit()

            return redirect(url_for('private.jinja'))
    except:
        return redirect(url_for('registerprivate'))
    return render_template('registerprivate.jinja')


@app.route('/registerpublic',methods=['POST','GET'])
def registerpublic():
    try:
        if (request.method == 'POST'):
            name=request.form.get('name')
            location = request.form.get('location')
            tuitionfee=request.form.get('tuitionfee')
            size=request.form.get('size')
            matriculation=request.form.get('matriculation')
            rank=request.form.get('rank')
            
            public=PublicSchools(name=name, location=location, tuitionfee=int(tuitionfee), size=size, matriculation=matriculation, rank=int(rank))
            db.session.add(public)
            db.session.commit()

            return redirect(url_for('public.jinja'))
    except:
        return redirect(url_for('registerpublic'))
    return render_template('registerpublic.jinja')

@app.route('/registerboarding',methods=['POST','GET'])
def registerboarding():
    try:
        if (request.method == 'POST'):
            name=request.form.get('name')
            location = request.form.get('location')
            tuitionfee=request.form.get('tuitionfee')
            size=request.form.get('size')
            matriculation=request.form.get('matriculation')
            rank=request.form.get('rank')
            
            boarding=BoardingSchools(name=name, location=location, tuitionfee=int(tuitionfee), size=size, matriculation=matriculation, rank=int(rank))
            db.session.add(boarding)
            db.session.commit()

            return redirect(url_for('boarding.jinja'))
    except:
        return redirect(url_for('registerboarding'))
    return render_template('registerboarding.jinja')

@app.route('/users')
def users():
    if (not session.get('user')):
        return redirect(url_for('index'))

    users= User.query.all()
    return render_template('users.jinja', users=users)

@app.route('/lr')
def lr():
    return render_template('lr.jinja')
@app.route('/private/<schoolname>',methods=['POST','GET'])
def privateschool(schoolname):
    if (not session.get('user')):
        return redirect(url_for('lr'))
    school=PrivateSchools.query.filter_by(name=schoolname ).first()
    name=school.name
    location=school.location
    tuitionfee=school.tuitionfee
    rank=school.rank
    size=school.size
    matriculation=school.matriculation
    already=''
    allrank=[]
    type=[]
    if (BoardingSchools.includes(name)):
        type.append('boardingschool')
    if (PrivateSchools.includes(name)):
        type.append('privateschool')
    if (PublicSchools.includes(name)):
        type.append('publicschool')
    if len(type)>1:
        boardings=BoardingSchools.query.all()
        publics=PublicSchools.query.all()

        for boarding in boardings:
            if name==boarding.name:
                allrank.append(['Boarding Rank',boarding.rank])
        
        for public in publics:
            if name==public.name:
                allrank.append(['Public Rank',public.rank])
        
        allrank.append(['Private Rank',rank])
    else:
        allrank.append(['Private Rank',rank])
    username=session.get('user')[0]
    user=User.query.filter_by(username=username ).first()
    hello=str(user.favorite).split(',')
    for thing in hello:
        if name == thing:
            already=True
            if (request.method=='POST'):
                if request.form.get('remove'):
                    hello.remove(name)
                    user.favorite=listToString(hello)
                    db.session.commit()
                    return redirect (url_for('profile'))
            return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)

    if (request.method=='POST'):
        if request.form.get('add'):
            if str(user.favorite)=='None':
                user.favorite=name
                user.favorite+=','
            else:
                user.favorite=str(user.favorite)+name
                user.favorite+=','
            db.session.commit()
            return redirect (url_for('profile'))
    return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)


@app.route('/public/<schoolname>',methods=['POST','GET'])
def publicschool(schoolname):
    if (not session.get('user')):
        return redirect(url_for('lr'))
    school=PublicSchools.query.filter_by(name=schoolname ).first()
    name=school.name
    location=school.location
    tuitionfee=school.tuitionfee
    rank=school.rank
    size=school.size
    matriculation=school.matriculation
    already=''
    allrank=[]
    type=[]
    if (BoardingSchools.includes(name)):
        type.append('boardingschool')
    if (PrivateSchools.includes(name)):
        type.append('privateschool')
    if (PublicSchools.includes(name)):
        type.append('publicschool')
    if len(type)>1:
        boardings=BoardingSchools.query.all()
        privates=PrivateSchools.query.all()

        for boarding in boardings:
            if name==boarding.name:
                allrank.append(['Boarding Rank',boarding.rank])
        
        for private in privates:
            if name==private.name:
                allrank.append(['Private Rank',private.rank])
        
        allrank.append(['Public Rank',rank])
    else:
        allrank.append(['Public Rank',rank])

    username=session.get('user')[0]
    user=User.query.filter_by(username=username ).first()
    hello=str(user.favorite).split(',')
    for thing in hello:
        if name == thing:
            already=True
            if (request.method=='POST'):
                if request.form.get('remove'):
                    hello.remove(name)
                    user.favorite=listToString(hello)
                    db.session.commit()
                    return redirect (url_for('profile'))
            return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)

    if (request.method=='POST'):
        if request.form.get('add'):
            if str(user.favorite)=='None':
                user.favorite=name
                user.favorite+=','
            else:
                user.favorite=str(user.favorite)+name
                user.favorite+=','
            db.session.commit()
            return redirect (url_for('profile'))
    return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)

@app.route('/boarding/<schoolname>',methods=['POST','GET'])
def boardingschool(schoolname):
    if (not session.get('user')):
        return redirect(url_for('lr'))
    school=BoardingSchools.query.filter_by(name=schoolname ).first()
    name=school.name
    location=school.location
    tuitionfee=school.tuitionfee
    rank=school.rank
    size=school.size
    matriculation=school.matriculation
    already=False
    allrank=[]
    type=[]
    if (BoardingSchools.includes(name)):
        type.append('boardingschool')
    if (PrivateSchools.includes(name)):
        type.append('privateschool')
    if (PublicSchools.includes(name)):
        type.append('publicschool')
    if len(type)>1:
        privates=PrivateSchools.query.all()
        publics=PublicSchools.query.all()

        for private in privates:
            if name==private.name:
                allrank.append(['Private Rank',private.rank])
        
        for public in publics:
            if name==public.name:
                allrank.append(['Public Rank',public.rank])
        
        allrank.append(['Boarding Rank',rank])
    else:
        allrank.append(['Boarding Rank',rank])
    
    username=session.get('user')[0]
    user=User.query.filter_by(username=username ).first()
    hello=str(user.favorite).split(',')
    for thing in hello:
        if name == thing:
            already=True
            if (request.method=='POST'):
                if request.form.get('remove'):
                    hello.remove(name)
                    user.favorite=listToString(hello)
                    db.session.commit()
                    return redirect (url_for('profile'))
            return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)

    if (request.method=='POST'):
        if request.form.get('add'):
            if str(user.favorite)=='None':
                user.favorite=name
                user.favorite+=','
            else:
                user.favorite=str(user.favorite)+name
                user.favorite+=','
            db.session.commit()
            return redirect (url_for('profile'))
    return render_template('school.jinja',name=name,location=location,tuitionfee=tuitionfee,rank=rank,matriculation=matriculation,size=size, already=already, allrank=allrank)


@app.route('/private')
def private():
    privates= PrivateSchools.query.all()
    privates_sorted = sorted(privates, key = lambda x: x.rank)

    return render_template('private.jinja', privates=privates,privateschools=privates_sorted)

@app.route('/public')
def public():
    publics= PublicSchools.query.all()
    public_sorted = sorted(publics, key = lambda x: x.rank)
    return render_template('public.jinja', publics=publics,publicschools=public_sorted)

@app.route('/boarding')
def boarding():
    boardings= BoardingSchools.query.all()
    boarding_sorted = sorted(boardings, key = lambda x: x.rank)
    return render_template('boarding.jinja', boardings=boardings,boardingschools=boarding_sorted)


@app.route('/login',methods=['POST','GET'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        users=User.query.all()
        for user in users:
            if username==user.username:
                if password==user.password:
                    session['user'] = [user.username, user.password, user.firstname, user.lastname, user.money]
                    return redirect (url_for('index'))

    return render_template('login.jinja')
            





@app.route('/profile',methods=['POST','GET'])

def profile():
    no=''
    if (not session.get('user')):
        return redirect(url_for('index'))
    
    name=session.get('user')[0]
    user=User.query.filter_by(username=name ).first()
    favorite=str(user.favorite)
    hello=favorite.split(',')[:-1]
    print('hello = {}'.format(hello))
    schools=[]
    boardingschools=[]
    publicschools=[]
    privateschools=[]
    if len(hello)==0:
        no='You Do Not Have Any Favorite School Yet'
    for thing in hello:
        school_type = []
        print(thing)
        print('no school type yet')
        if (BoardingSchools.includes(thing)):
            print('is boarding')
            school_type.append('boardingschool')
        if (PublicSchools.includes(thing)):
            print('is public')
            school_type.append('publicschool')
        if (PrivateSchools.includes(thing)):
            print('is private')
            school_type.append('privateschool')
            
        schools.append([thing,school_type])
    
    for school in schools:
        for type in school[1]:
            if type=='boardingschool':
                boardingschools.append([school[0],type])
            if type=='publicschool':
                publicschools.append([school[0],type])
            if type=='privateschool':
                privateschools.append([school[0],type])

    print(schools)
    print(privateschools)
    print(boardingschools)
    print(publicschools)
    return render_template('profile.jinja',favorite=favorite,hello=hello,schools=schools, no=no, privateschools=privateschools, boardingschools=boardingschools, publicschools=publicschools)


@app.route('/money',methods=['POST','GET'])

def money():
    if (not session.get('user')):
        return redirect(url_for('index'))
    name=session.get('user')[0]
    user=User.query.filter_by(username=name ).first()
    money=user.money

    if (request.method=='POST'):

        if request.form.get('depositbutton'):
            try:
                deposit = int(request.form.get('deposit'))
                if deposit<0:
                    return redirect(url_for('money'))
                user.money += deposit
                db.session.commit()
                return redirect(url_for('money'))
            except:
                return redirect(url_for('money'))

        if request.form.get('withdrawbutton'):
            try:

                withdraw = int(request.form.get('withdraw'))
                if withdraw<0:
                    return redirect(url_for('money'))
                user.money -= withdraw
                db.session.commit()
                return redirect(url_for('money'))
            except:
                return redirect(url_for('money'))
            
    return render_template('money.jinja', user=user, money=money)



@app.route('/logout')
def logout():
    if (not session.get('user')):
        return redirect(url_for('index'))
    session['user'] = None
    return redirect(url_for('index'))



if __name__ == "__main__":
    db.create_all()
    app.run()


