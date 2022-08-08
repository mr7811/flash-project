from flask import Flask, request , jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model


app = Flask(__name__)

db = PostgresqlDatabase(
    'people', 
    user= 'timothytang',
    password ='',
    host='localhost',
    port= 5432
)

class BaseModel(Model):
    class Meta:
        database = db
class Person(BaseModel):
    name = CharField()
    age = IntegerField()

db.connect()
db.drop_tables([Person])
db.create_tables([Person])

Person(name='Tim', age=100).save()
Person(name='Mack', age=100).save()

app.run(debug=True)