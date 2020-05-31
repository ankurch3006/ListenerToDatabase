import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import mysql.connector as mariadb
import pandas as pd
import os
import smtplib

class ListenerHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]

    def sendEmail(self, message):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.connect('smtp.gmail.com', 587)
        mail.starttls()
        sender = ""
        password = ''
        mail.login(sender, password)
        mail.sendmail(sender, 'ankurch3006@gmail.com', message)
    
    def process(self, event):
        try:
            conn = mariadb.connect(user="root", password="root", host="127.0.0.1", port=3306, database = 'schedule')
            cursor = conn.cursor()
            path_csv = os.path.abspath(event.src_path).replace('\\', '/')
            df = pd.read_csv(path_csv)
            for data in df.columns:
                for d in df[data]:
                    query = "INSERT INTO `names` (`column`) VALUES (%s)"
                    cursor.execute(query,(d,))
            conn.commit()
            print("completed!!")
        
        except Exception as e:
            self.sendEmail(e.msg)
            print(e.msg)
            
        finally:
            cursor.close()
            conn.close()
        
    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    path = "C:/Users/ankur/Desktop/Scheduling_python/X"
    observer = Observer()
    observer.schedule(ListenerHandler(), path if path else '.')
    observer.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        
    observer.join()