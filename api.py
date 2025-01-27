from flask import Flask, jsonify, request
from waitress import serve
import requests as req
import dotenv
import os

# Load environment variables from a .env file
dotenv.load_dotenv()
# Retrieve environment variables for host, port, and Discord webhook
HOST = str(os.getenv('HOST'))
PORT = os.getenv('PORT')
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
        print('send_discord_message: Alerta enviado!')
        print(message)
    else:
        print('send_discord_message: Erro ao enviar mensagem:', response.text)

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

# Function to print application startup information
def init():
    info = f'''Aplicação Iniciada:
    Rodando em: {HOST}:{PORT}
{'='*30}'''
    print(info)

# Route to handle POST requests from Uptime Kuma
@app.route('/uptimekuma', methods=['POST'])
def uptimekuma():
    return route_uptimekuma()

# Root route to display basic application info
@app.route('/')
def index():
    return f'''<h1>Aplicação Iniciada:</h1><h2>Rodando em: {HOST}:{PORT}</h2>'''

# Entry point of the application
if __name__ == '__main__':
    init()
    # Start the Flask app using Waitress as the production WSGI server
    serve(app, host=HOST, port=PORT)
