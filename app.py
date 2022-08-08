from flask import Flask, request , jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model


app = Flask(__name__)

db = PostgresqlDatabase(
    'pokemon', 
    user= 'timothytang',
    password ='',
    host='localhost',
    port= 5432
)

class BaseModel(Model):
    class Meta:
        database = db

class Pokemon(BaseModel):
    name = CharField()
    age = IntegerField()
    ele = CharField()

db.connect()
db.drop_tables([Pokemon])
db.create_tables([Pokemon])

Pokemon(name='Squirtle', age=100, ele='water').save()
Pokemon(name='Charizard', age=100, ele ='fire').save()

@app.route('/pokemon/', methods= ['GET', 'POST'])
@app.route('/pokemon/<id>', methods= ['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(
                model_to_dict(
                    Pokemon.get(
                        Pokemon.id == id
                    )
                )
            )
        else:
            pokemon_list=[]
            for pokemon in Pokemon.select():
                pokemon_list.append(model_to_dict(pokemon))
            return jsonify(pokemon_list)

    if request.method =='PUT':
        body = request.get_json()
        Pokemon.update(body).where(Pokemon.id == id).execute()
        return "Pokemon " + str(id) + " has been updated."

    if request.method == 'POST':
        new_pokemon = dict_to_model(Pokemon, request.get_json())
        new_pokemon.save()
        return jsonify({'successfuly posted': True})

    if request.method == 'DELETE':
        Pokemon.delete().where(Pokemon.id == id).execute()
        return "Pokemon " + str(id) + " deleted."
app.run(debug=True, port = 5000)