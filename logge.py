from datetime import datetime
def generate_log(content):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y %H:%M:%S")
    print(date)
    with open('/home/pi/zlogs.txt','a') as f:
        f.write(f'{date}::{content}\n')
