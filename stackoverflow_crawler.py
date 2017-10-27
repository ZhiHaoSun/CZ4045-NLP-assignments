# -*- coding: utf-8 -*-

import sys
import requests
from Queue import Queue, Empty
from threading import Thread
import json
import bs4
import time

reload(sys)  
sys.setdefaultencoding('utf8')
queue = Queue()
result = []

base = "https://stackoverflow.com/questions/tagged/java?sort=frequent&pagesize=50&page="

headers = {
    'Cache-Control' : 'no-cache',
    'Cookie' : '',
    'Connection' : 'keep-alive'
}

def process(content):
    soup = bs4.BeautifulSoup(content, "html.parser")

    # process the html content
    questions = soup.find_all('div' , class_="question-summary")

    for question in questions:
        answer_count = int(question.find('div', class_="status").find('strong').text)
        if (answer_count > 2):
            question_link = question.find('a', class_="question-hyperlink").get("href")
            result.append(question_link)
    

def get_parser():

    def parse():
        try:
            while True:
                page = queue.get_nowait()
                link = base + str(page)

                r = requests.get(link, verify=False, headers = headers)

                try:
                    process(r.text.encode('utf-8'))
                except Exception:
                    print page
                time.sleep(100)
        except Empty:
            pass

    return parse


parser = get_parser()

for i in range(1 , 13):
    queue.put(i)

workers = []
for i in range(10): # number of threads
    worker = Thread(target=parser)
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()

print "total count:" + str(len(result))
write_file = open('stackoverflow_questions' , 'w+')
write_file.write("\n".join(result))
