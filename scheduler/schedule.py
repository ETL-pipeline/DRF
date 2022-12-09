# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoJobStore
# from .bot import bot_schedule

# def start():
#     scheduler=BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
#     register_events(scheduler)
#     @scheduler.scheduled_job('cron', minute = '*/30', name = 'auto')
#     def auto_check():
#         bot_schedule(5)
#     scheduler.start()

