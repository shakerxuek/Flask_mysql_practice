from time import time
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:XK5213986@localhost:3306/our_users'
db = SQLAlchemy(app)

###Models####
class Logs(db.Model):
    # __tablename__ = "outputs"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20))
    sessionid = db.Column(db.String(100))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,userid,sessionid):
        self.userid = userid
        self.sessionid = sessionid
    def __repr__(self):
        return '' % self.id

class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time=db.Column(db.String(20))
    type=db.Column(db.String(20))
    properties=db.Column(db.String(20))
    user_id=db.Column(db.String(20),db.ForeignKey('logs.id'))  
    user=db.relationship('Logs',backref='actions')

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,time,type,properties,user):
        self.time = time
        self.type = type
        self.properties = properties
        self.user = user
    def __repr__(self):
        return '' % self.id

db.create_all()
test=Logs(userid='1',sessionid='2')
ac1=Actions(time='1',type='CLICK',properties='xxx',user=test)
ac1.create()
class LogsSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Logs
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    userid = fields.String(required=True)
    sessionid = fields.String(required=True)

class actionSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Actions
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    time = fields.String(required=True)
    type = fields.String(required=True)
    properties = fields.String(required=True)

@app.route('/', methods = ['GET'])
def index():
    get_Logs = Logs.query.all()
    Logs_schema = LogsSchema(many=True)
    logs = Logs_schema.dump(get_Logs)
    return make_response(jsonify({"log": logs}))
@app.route('/Logs/<id>', methods = ['GET'])
def get_Logs_by_id(id):
    get_Logs = Logs.query.get(id)
    Logs_schema = LogsSchema()
    log = Logs_schema.dump(get_Logs)
    return make_response(jsonify({"log": log}))
@app.route('/Logs/<id>', methods = ['PUT'])
def update_Log_by_id(id):
    data = request.get_json()
    get_Logs = Logs.query.get(id)
    if data.get('userid'):
        get_Logs.userid = data['userid']
    if data.get('sessionid'):
        get_Logs.sessionid = data['sessionid']
    if data.get('actions'):
        get_Logs.actions = data['actions'] 
    db.session.add(get_Logs)
    db.session.commit()
    Logs_schema = LogsSchema(only=['id', 'userid', 'sessionid','actions'])
    Log = Logs_schema.dump(get_Logs)
    return make_response(jsonify({"log": Log}))
@app.route('/Logs/<id>', methods = ['DELETE'])
def delete_Logs_by_id(id):
    get_Logs = Logs.query.get(id)
    db.session.delete(get_Logs)
    db.session.commit()
    return make_response("",204)
@app.route('/Logs', methods = ['POST'])
def create_Logs():
    data = request.get_json()
    Logs_schema = LogsSchema()
    Logs = Logs_schema.load(data)
    result = Logs_schema.dump(Logs.create())
    return make_response(jsonify({"log": result}),200)
if __name__ == "__main__":
    app.run(debug=True)

