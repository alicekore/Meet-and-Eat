from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import deleteEvents, makeEventsInvisible

def start():
    scheduler = BackgroundScheduler()
    minutes_per_day = 60*24
    minutes_per_week = 60*24*7
    scheduler.add_job(deleteEvents, 'interval', minutes=minutes_per_week)
    scheduler.add_job(makeEventsInvisible, 'interval', minutes=minutes_per_week)
    scheduler.start()