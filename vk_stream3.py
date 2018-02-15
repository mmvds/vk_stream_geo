#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from vkstreaming import Streaming
import postgresql
db = postgresql.open('pq://<dbuser>:<dbpassword>@localhost:5432/<dbname>')
ins = db.prepare("INSERT INTO stream (is_post, user_id,post_id,tags,text,creation_time) VALUES ($1, $2, $3, $4, $5, $6)")

if __name__ == '__main__':
    api = Streaming("streaming.vk.com", "<VKStreamAPIToken>")

    api.del_all_rules()
    api.add_rules("K", "хорошо")
    #api.add_rules("B1", "навальный")
    #api.add_rules("B2", "приболел")
    #api.add_rules("B3", "грипп")
    #api.add_rules("B4", "простуда")
    #api.add_rules("B5", "выздоравливай")

    rules = api.get_rules()
    for rule in rules:
        print(("{tag:15}:{value}").format(**rule))

    @api.stream
    def my_func(event):
        if int(event['author']['id'])>0:
          if event['event_type']!='share':
             if len(event['text'])<500:
                print("{} [{}|{}]: {} : {}".format(event['event_type'],event['author']['id'], event['event_id']['post_id'], event['tags'], event['text']))
                if (event['event_type']=='post'):
                  ins(True,str(event['author']['id']),str(event['event_id']['post_id']),str(event['tags']),str(event['text']),int(event['creation_time']))
                else:
                  ins(False,str(event['author']['id']),str(event['event_id']['post_id']),str(event['tags']),str(event['text']),int(event['creation_time']))
    api.start()

