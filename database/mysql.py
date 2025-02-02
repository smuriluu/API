import pymysql
import dotenv
import os
from log.log import logging
from flask import jsonify

# Load environment variables from a .env file
dotenv.load_dotenv()
HOST = str(os.getenv('MYSQL_HOST'))
OWNER = str(os.getenv('MYSQL_OWNER'))
PASSWORD = str(os.getenv('MYSQL_PASSWORD'))
DATABASE = str(os.getenv('MYSQL_DATABASE'))

def query_sing_in(username, password):
    try:
        with pymysql.connect(
            host=HOST,
            user=OWNER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            with connection.cursor() as cur:
                sql = f'select id, username, password from users where username = "{username}" and password = "{password}"'
                cur.execute(sql)
                result = cur.fetchone()
                if result:
                    return {
                        'id': result[0],
                        'username': result[1],
                        'password': result[2]
                    }
                else:
                    return True
    except Exception as error:
        logging.error(f'MYSQL query_sing_in: {error}')
        return False

def query_verify_users(username):
    try:
        with pymysql.connect(
            host=HOST,
            user=OWNER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            with connection.cursor() as cur:
                sql = f'select username from users where username = "{username}"'
                cur.execute(sql)
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    return True
    except Exception as error:
        logging.error(f'MYSQL query_verify_users: {error}')
        return False

# Function to insert a new user into the database
def insert_users(username, password):
    try:
        # Establish a connection inside the function
        with pymysql.connect(
            host=HOST,
            user=OWNER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            with connection.cursor() as cur:
                sql = f'insert into users (username, password, admin, active) values ("{username}", "{password}", 0, 1)'
                cur.execute(sql)
                connection.commit()
                return True
    except Exception as error:
        logging.error(f'MYSQL insert_users: {error}')
        return False

### ROUTES ###

def route_new_user(data):
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    query_result = query_verify_users(username)
    if username == '' or password == '' or confirm_password == '':
        return jsonify({'error_code': '02'}), 400
    elif password != confirm_password:
        return jsonify({'error_code': '03'}), 422
    elif any(char in username for char in  ' !@#$%^&*()/?:"<>|,.;'):
        return jsonify({'error_code': '04'}), 422
    elif username[0] in '0123456789':
        return jsonify({'error_code': '05'}), 422
    elif query_result == username:
        return jsonify({'error_code': '06'}), 422
    elif not query_result:
        return jsonify({'error_code': '01'}), 500
    
    insert_result = insert_users(username, password)
    if insert_result:
        return jsonify({'msg_code': '01'}), 201
    else:
        return jsonify({'error_code': '01'}), 500

def route_sing_in(data):
    username = data.get('username')
    password = data.get('password')
    if username == '' or password == '':
        return jsonify({'error_code': '07'}), 400

    query_result = query_sing_in(username, password)
    if not query_result:
        return jsonify({'error_code': '01'}), 500
    else:
        try:
            return jsonify({'id': query_result['id']}), 200
        except Exception as msg:
            return jsonify({'msg_code': '02'}), 200
