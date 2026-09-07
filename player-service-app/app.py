from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from player_service import PlayerService
import ollama

app = Flask(__name__)

# Load CSV file in pandas dataframe and create SQLite database
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, 'Player.csv'))
engine = create_engine('sqlite:///player.db', echo=True)
df.to_sql('players', con=engine, if_exists='replace', index=False)

# Get all players
@app.route('/v1/players', methods=['GET'])
def get_players():
   with PlayerService() as svc:
        country = request.args.get('birthCountry')
        if country:
            players = svc.search_by_country(country)
            return jsonify(players)
        else:
            return jsonify(svc.get_all_players())

@app.route('/v1/players/<string:player_id>')
def query_player_id(player_id):
    with PlayerService() as svc:
        result = svc.search_by_player(player_id)

    if len(result) == 0:
        return jsonify({"error": "No record found with player_id={}".format(player_id)})
    else:
        return jsonify(result)

@app.route('/v1/chat/list-models')
def list_models():
    return jsonify(ollama.list())

@app.route('/v1/chat', methods=['POST'])
def chat():
    # Process the data as needed
    response = ollama.chat(model='tinyllama', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
