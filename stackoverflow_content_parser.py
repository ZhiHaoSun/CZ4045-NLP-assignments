# -*- coding: utf-8 -*-

import sys
import requests
from Queue import Queue, Empty
import multiprocessing
from threading import Thread
import json
import bs4
import time
from os.path import abspath, exists
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

reload(sys)  
sys.setdefaultencoding('utf8')
queue = Queue()
result = []

base = "https://stackoverflow.com"

headers = {
    'Cache-Control' : 'no-cache',
    'Cookie' : '',
    'Connection' : 'keep-alive'
}

output_path = abspath("stackoverflow_content")
lock = multiprocessing.Lock()
def process(content):
    soup = bs4.BeautifulSoup(content, "html.parser")

    # process the html content
    posts = soup.find_all('div' , class_="post-text")
    print len(posts)
    if len(posts) == 0:
        print content

    with lock:
        try:
            output_file = open(output_path, 'a')
            output_file.write("\n\n\n\n")
            for post in posts:
                for post_content in post.find_all('p'):
                    output_file.write(post_content.text + "\n\n\n")
        except Exception, e:
                print str(e)

def get_parser():

    def parse():
        try:
            while True:
                question_link = queue.get_nowait().strip()
                link = base + question_link

                print link
                r = requests.get(link, verify=False, headers = headers)

                try:
                    process(r.text.encode('utf-8'))
                except Exception, e:
                    print str(e)
                    print question_link
                time.sleep(2000)
        except Empty:
            pass

    return parse


parser = get_parser()

questions_path = abspath("stackoverflow_questions")
if exists(questions_path):
    with open(questions_path) as question_file:
        for line in question_file:
            queue.put(line)

workers = []
for i in range(60): # number of threads
    worker = Thread(target=parser)
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()

