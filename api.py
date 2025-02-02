from flask import Flask, request
from waitress import serve
import requests as req
import dotenv
import os
from database.mysql import route_new_user, route_sing_in
from log.log import logging

# Load environment variables from a .env file
dotenv.load_dotenv()
# Retrieve environment variables for host, port, and Discord webhook
HOST = str(os.getenv('API_HOST'))
PORT = os.getenv('API_PORT')
DISCORD_WEBHOOK = str(os.getenv('DISCORD_WEBHOOK'))

# Initialize the Flask app
app = Flask(__name__)

# Function to send a message to a Discord webhook
def send_discord_message(message):
    webhook_url = DISCORD_WEBHOOK
    data = {'content': message}
    response = req.post(webhook_url, json=data)
    # Status code 204 means success
    if response.status_code == 204:
        logging.info('send_discord_message: Alerta enviado!')
        logging.info(message)
    else:
        logging.info('send_discord_message: Erro ao enviar mensagem:', response.text)

# Function to handle the logic for the `/uptimekuma` route
def route_uptimekuma():
    # Get JSON payload from the POST request
    data = request.get_json()
    info = f'''ALERTA MONITORAMENTO HOST1
    Servico: {data['resource']}
    {data['text']}
{'='*30}'''
    send_discord_message(info)
    return data

# Function to logging.info application startup information
def init():
    info = f'''Aplicacao Iniciada:
    Rodando em: {HOST}:{PORT}
{'='*30}'''
    logging.info(info)

# Route to insert a new user
@app.route('/new-user', methods=['POST'])
def new_user():
    data = request.get_json()
    return route_new_user(data)

@app.route('/sing-in', methods=['POST'])
def sing_in():
    data = request.get_json()
    return route_sing_in(data)

# Route to handle POST requests from Uptime Kuma
@app.route('/uptimekuma', methods=['POST'])
def uptimekuma():
    return route_uptimekuma()

# Root route to display basic application info
@app.route('/')
def index():
    return f'''<h1>Aplicacao Iniciada:</h1><h2>Rodando em: {HOST}:{PORT}</h2>'''

# Entry point of the application
if __name__ == '__main__':
    init()
    # Start the Flask app using Waitress as the production WSGI server
    serve(app, host=HOST, port=PORT)
