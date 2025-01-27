import pymysql
import dotenv
import os
from log.log import logging

# Load environment variables from a .env file
dotenv.load_dotenv()
HOST = str(os.getenv('MYSQL_HOST'))
OWNER = str(os.getenv('MYSQL_OWNER'))
PASSWORD = str(os.getenv('MYSQL_PASSWORD'))
DATABASE = str(os.getenv('MYSQL_DATABASE'))

# Establish a connection to the MySQL database
db = pymysql.connect(
    host=HOST,
    user=OWNER,
    password=PASSWORD,
    database=DATABASE
)
# Create a cursor object to interact with the database
cur = db.cursor()

# Function to query users by their ID
def query_users(id):
    try:
        sql = f'select username, password, admin from users where id={id}'
        cur.execute(sql)
    except Exception as error:
        logging.info(error)
        return False
    else:
        return cur.fetchall()[0]

# Function to insert a new user into the database
def insert_users(username, password):
    try:
        sql = f"insert into users (username, password, admin, active) values ('{username}', '{password}', 0, 1)"
        cur.execute(sql)
        db.commit()
    except Exception as error:
        logging.info(error)
        return False
    else:
        return True
