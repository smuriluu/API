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
                sql = 'select id, active from users where username = %s and password = %s'
                params = (username, password)
                cur.execute(sql, params)
                result = cur.fetchone()
                if result:
                    return {
                        'id': result[0],
                        'active': result[1]
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
                sql = 'select username from users where username = %s'
                params = (username)
                cur.execute(sql, params)
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    return True
    except Exception as error:
        logging.error(f'MYSQL query_verify_users: {error}')
        return False

def query_users_verify_session(id):
    try:
        with pymysql.connect(
            host=HOST,
            user=OWNER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            with connection.cursor() as cur:
                sql = 'select session_last_seen from users where id = %s'
                params = (id)
                cur.execute(sql, params)
                result = cur.fetchone()
                if result[0]:
                    return False
                else:
                    return True
    except Exception:
        return False

def insert_users_new_session(id):
    from datetime import datetime
    if query_users_verify_session(id):
        try:
            with pymysql.connect(
                host=HOST,
                user=OWNER,
                password=PASSWORD,
                database=DATABASE
            ) as connection:
                with connection.cursor() as cur:
                    sql = 'update users set session_last_seen = %s where id = %s'
                    params = (datetime.now(), id)
                    cur.execute(sql, params)
                    connection.commit()
                    return True
        except Exception as error:
            logging.error(f'MYSQL insert_users_new_session: {error}')
            return False
    else:
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
                sql = 'insert into users (username, password, admin, active, creation_date) values (%s, %s, 0, 1, sysdate())'
                params = (username, password)
                cur.execute(sql, params)
                connection.commit()
                return True
    except Exception as error:
        logging.error(f'MYSQL insert_users: {error}')
        return False

def clean_expired_session():
    from datetime import datetime, timedelta
    try:
        with pymysql.connect(
            host=HOST,
            user=OWNER,
            password=PASSWORD,
            database=DATABASE
        ) as connection:
            with connection.cursor() as cur:
                sql = 'update users set session_id = NULL, session_last_seen = NULL where session_last_seen < %s'
                params = (datetime.now() - timedelta(minutes=1))
                cur.execute(sql, params)
                connection.commit()
    except Exception as error:
        logging.error(f'MYSQL clean_expired_session: {error}')

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
            if query_result['active'] == 0:
                return jsonify({'msg_code': '03'}), 200
            else:
                if insert_users_new_session(query_result['id']):
                    return jsonify({'id': query_result['id']}), 200
                else:
                    return jsonify({'error_code': '08'}), 400
        except Exception:
            return jsonify({'msg_code': '02'}), 200
