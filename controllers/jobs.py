from apscheduler.schedulers.background import BackgroundScheduler
import atexit

def verify_expired_session():
    from database.mysql import clean_expired_session
    clean_expired_session()

scheduler = BackgroundScheduler()
scheduler.add_job(func=verify_expired_session, trigger='interval', minutes=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())