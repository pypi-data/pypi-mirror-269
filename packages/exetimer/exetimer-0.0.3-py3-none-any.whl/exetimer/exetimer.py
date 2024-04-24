import datetime, atexit

st = datetime.datetime.now()

def end_timer():
    et = datetime.datetime.now()
    elapsed_time = et - st
    print('\n\nTotal execution time:', elapsed_time, '\n')

atexit.register(end_timer)