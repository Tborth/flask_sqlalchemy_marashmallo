from operator import methodcaller
from flask import Flask,jsonify,request,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, ForeignKey, Sequence
from flask_marshmallow import Marshmallow
from marshmallow import Schema, ValidationError, fields, post_load, INCLUDE,validates,validate
from werkzeug.utils import redirect
from sqlalchemy.sql.schema import ForeignKeyConstraint

import json
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Planbookingheader(db.Model):

    __tablename__ = 'planbookingheader'
    # __table_args__ = (db.UniqueConstraint('projectid'), )

    projectid = db.Column(db.Integer, primary_key=True, nullable=False)

    awb = db.Column(db.String(128), primary_key=True)

    origin = db.Column(db.String(30), default='')
  
    lastupdatedt = db.Column(db.DateTime, default=func.now(), nullable=False)


class Planbookingdtlines(db.Model):

    __tablename__ = 'planbookingdtlines'

    
    """ This is foreign key """

    projectid = db.Column(db.Integer, primary_key=True, nullable=False)

    source = db.Column(db.String(128))

    awb = db.Column(db.String(128),  nullable=False)

    lastupdatedt = db.Column(db.DateTime, default=func.now(), nullable=False)    

    __table_args__ = (ForeignKeyConstraint([projectid, awb],
                                    [Planbookingheader.projectid, Planbookingheader.awb]),
                {})
    



class Myapp(db.Model):
    order_id = db.Column(db.Integer,primary_key =True)
    size = db.Column(db.String(500))
    toppings= db.Column(db.String(500))
    crust = db.Column(db.String(500))

class Owner(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    address =db.Column(db.String(100))
    # pets =db.relationship('Pet',backref='owner')

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer , primary_key =True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    owner_id =db.Column(db.Integer)

    __table_args__ = (ForeignKeyConstraint([owner_id],[Owner.id]), {})


@app.route('/owner/<id>', methods=['PUT'])
def put_Owner(id):

    req = request.get_json()
    # input_dic['id']=req['id']
    input_dic['id'] = req['id']
    input_dic['name'] = req['name']
    input_dic['address']=req['address']


    # input_dic['crust']  = req['crust']
    # order_id= req['order_id']
    # size = req['size']
    # toppings = req['toppings']
    print("=--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # crust = req['crust']
    print(input_dic)
    # new_entry=MyAppSchema().load(json.loads(json.dumps(input_dic)))
    # tool=Owner(name=input_dic['name'], address=input_dic['address'])
    owner_id=Owner.query.get(id)
    owner_id.id=input_dic['id'] 
    owner_id.name =input_dic['name']
    owner_id.address =input_dic['address']

    db.session.add(owner_id )
    # try:
      
    db.session.commit()
    # except ValidationError as err:
    #     print(err)
    #     print(err.valid_data)
    return "Hello world"



@app.route('/owner', methods=['POST'])
def post_Owner():

    req = request.get_json()
    # input_dic['id']=req['id']
    input_dic['name'] = req['name']
    input_dic['address'] = req['address']
    # input_dic['crust']  = req['crust']
    # order_id= req['order_id']
    # size = req['size']
    # toppings = req['toppings']
    print("=--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # crust = req['crust']
    print(input_dic)
    # new_entry=MyAppSchema().load(json.loads(json.dumps(input_dic)))
    tool=Owner(name=input_dic['name'], address=input_dic['address'])

    db.session.add( tool )
    # try:
      
    db.session.commit()
    # except ValidationError as err:
    #     print(err)
    #     print(err.valid_data)
    return "Hello world"


@app.route('/pet/<owner_Id>', methods=['POST'])
def post_pet(owner_Id):

    req = request.get_json()
    # input_dic['id']=req['id']
    input_dic['name'] = req['name']
    input_dic['age'] = req['age']
    # input_dic['owner_id'] = req['owner_id'] 
    # input_dic['crust']  = req['crust']
    # order_id= req['order_id']
    # size = req['size']
    # toppings = req['toppings']
    print("=--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # crust = req['crust']
    print(input_dic)
    # new_entry=MyAppSchema().load(json.loads(json.dumps(input_dic)))
    tool=Pet(name=input_dic['name'], age=input_dic['age'],owner_id=owner_Id)

    db.session.add( tool )
    # try:
      
    db.session.commit()
    # except ValidationError as err:
    #     print(err)
    #     print(err.valid_data)
    return "Hello world"

@app.route('/owner')
def get_owner():
    print(request.url)
    entries = Owner.query.all()
    print(entries)
    print("=====entries=============>>>>>>>")
    for i in entries:
        print(i.name)
        print(i.id)
    result="Hello worl"
    # result = my_app_schema.dump(entries)
    print("========>>>>>>>>>>>>result----->>>>>>>>>>>>>>>>>>>>>>>")
    print(result)
    return jsonify(result)

@app.route('/pet')
def get_pet():
    print(request.url)
    entries = Pet.query.all()
    print(entries)
    print("=====entries=============>>>>>>>")
    for i in entries:
        print(i.name)
        print(i.id)
        print(i.owner_id)
    result="Hello world"
    # result = my_app_schema.dump(entries)
    print("========>>>>>>>>>>>>result----->>>>>>>>>>>>>>>>>>>>>>>")
    print(result)
    return jsonify(result)


class MyAppSchema(ma.Schema):
   
    
    order_id = fields.Integer()
    size = fields.String()
    toppings = fields.String()
    crust = fields.String(validate=validate.Length(max=5))
      
    class Meta:
        model = Myapp
        fields = ('order_id','size','toppings','crust')
    @post_load
    def create_myapp(self,data,**kwargs):
        print("---data----")
        print(data)
        return Myapp(**data)


my_app_schema = MyAppSchema(many=True)

@app.route('/')
def hello_world():
    return 'Hellow world'

@app.route('/order')
def get_order():
    print(request.url)
    entries = Myapp.query.all()
    print(entries)
    print("=====entries=============>>>>>>>")
    print(entries[0].order_id)
    result = my_app_schema.dump(entries)
    print("========>>>>>>>>>>>>result----->>>>>>>>>>>>>>>>>>>>>>>")
    print(result)
    return jsonify(result)

input_dic={}



@app.route('/order', methods=['POST'])
def post_order():

    req = request.get_json()
    input_dic['order_id']=req['order_id']
    input_dic['size'] = req['size']
    input_dic['toppings'] = req['toppings']
    input_dic['crust']  = req['crust']
    # order_id= req['order_id']
    # size = req['size']
    # toppings = req['toppings']
    print("=--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # crust = req['crust']
    print(input_dic)
    new_entry=MyAppSchema().load(json.loads(json.dumps(input_dic)))
    db.session.add(new_entry)
    try:
      
        db.session.commit()
    except ValidationError as err:
        print(err)
        print(err.valid_data)

    # new_entry =Myapp(order_id = order_id , size=size, toppings=toppings,crust=crust)
   
    return redirect(url_for('get_order'))

@app.route('/order/<order_id>',methods=["PUT"])
def update_order(order_id):
    req = request.get_json()
    entry = Myapp.query.get(order_id)
    entry.size = req['size']
    entry.crust = req['crust']
    entry.toppings = req['toppings']
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('get_order'))

@app.route('/order/<order_id>',methods=['DELETE'])
def delete_order(order_id):
    entry = Myapp.query.get_or_404(order_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("get_order"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=6001)