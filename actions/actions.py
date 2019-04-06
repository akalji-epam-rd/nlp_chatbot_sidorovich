# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
import pymongo
import datetime
import time
from bson.objectid import ObjectId
from pymongo import MongoClient
import pprint
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

logger = logging.getLogger(__name__)

def get_time():
    ts = time.time()
    return ts

class StalkerAnecdote(Action):
    def name(self):
        return 'tell_an_anecdote'
    def run(self, dispatcher, tracker, domain):
        theme = tracker.get_slot('anecdote_theme')
        dispatcher.utter_message('funny anecdote with ' + theme)
        #dispatcher.utter_template('utter_joke')
        return []

class MemoryVisit(Action):
    def name(self):
        return "memory_visit"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        connection = MongoClient("ds127376.mlab.com", 27376)
        db = connection["chatbot"]
        db.authenticate("rasaguy", "rasabot1")
        collection = db['visiting']
        time_list = list(collection.find({}))
        posts = db.visiting
        
        uid = tracker.get_slot('id')
        if(uid is None):
            user_id = len(time_list) + 1
            
            
            st = datetime.datetime.fromtimestamp(get_time()).strftime('%Y-%m-%d %H:%M')
            print(st)
            post = {"id": str(user_id),
                     "first_time": st}
            posts.insert_one(post)
            dispatcher.utter_message("Finally! A newcomer! I'm so tired of that ugly faces around")
            return [SlotSet('id', str(user_id))]
        else:
            u_inf = collection.find_one({"id": uid})
            first_time = u_inf['first_time']
            dispatcher.utter_message("Oooh, I remember your smily face. It was sooo long ago. Thanks Gods I still remember correct time. I've met you %s" % first_time)
        connection.close()
        return []
    
class AnswerQuestion(Action):
    def name(self):
        return "answer_question"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        info = tracker.get_slot('info')
        dispatcher.utter_message("Yea, I can tell you a lot of things about %s" % info)
        return []


class ActionFindHideaway(Action):
    def name(self):
        return "action_find_hideaway"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("You can hide in Yanov")
        return []


class ActionCheckHideaway(Action):
    def name(self):
        return "action_check_hideaway"

    def run(self, dispatcher, tracker, domain):

        station_name = tracker.get_slot('station_name')
        dispatcher.utter_message("You can't hide in " + station_name)
        return []


class ActionLastEmission(Action):
    def name(self):
        return "action_last_emission"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Last emission was 30 minutes ago")
        return []


class ActionFutureEmission(Action):
    def name(self):
        return "action_future_emission"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The emission will be in 50 minutes")
        return []