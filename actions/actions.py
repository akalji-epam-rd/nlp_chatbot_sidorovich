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
import random
from bson.objectid import ObjectId
from pymongo import MongoClient
import pprint
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

logger = logging.getLogger(__name__)


class StalkerAnecdote(Action):
    def name(self):
        return 'tell_an_anecdote'

    def run(self, dispatcher, tracker, domain):
        theme = tracker.get_slot('anecdote_theme')
        dispatcher.utter_message('There should be funny anecdote with ' + theme)
        dispatcher.utter_message('But take this instead')
        buttons = []
        laugh = ""
        for i in range(3):
            laugh = (laugh + "ha")
            title = (laugh)
            payload = ("/laugh")
            buttons.append({"title": title, "payload": payload})
        dispatcher.utter_button_template('utter_joke', buttons, tracker)
        return []


'''

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

'''


class AnswerQuestion(Action):
    def name(self):
        return "answer_question"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        info = tracker.get_slot('info')
        if (info is None):
            dispatcher.utter_message("Okey, what things do you want to find out about?")
        else:
            dispatcher.utter_message("Yea, I can tell you a lot of things about %s" % info)
        return []


class ActionFindHideaway(Action):
    def name(self):
        return "action_find_hideaway"

    def run(self, dispatcher, tracker, domain):
        connection = MongoClient("ds127376.mlab.com", 27376)
        db = connection["chatbot"]
        db.authenticate("rasaguy", "rasabot1")
        collection = db['stations']

        stations = [document['station_name'] for document in collection.find()]
        selected_station = random.choice(stations)
        dispatcher.utter_message("You can hide in {}".format(selected_station))
        connection.close()

        return []


class ActionCheckHideaway(Action):
    def name(self):
        return "action_check_hideaway"

    def run(self, dispatcher, tracker, domain):
        is_can = random.choice([True, False])
        if is_can:
            dispatcher.utter_template("utter_can_hide", tracker)
        else:
            dispatcher.utter_template("utter_cant_hide", tracker)

        return []


class ActionLastEmission(Action):
    def name(self):
        return "action_last_emission"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Last emission was {} minutes ago".format(datetime.datetime.today().minute))
        return []


class ActionFutureEmission(Action):
    def name(self):
        return "action_future_emission"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("The emission will be in {} minutes".format(60 - datetime.datetime.today().minute))
        return []


class ActionBuy(Action):
    def name(self):
        return "action_buy"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        money = tracker.get_slot('money')
        if (money is None):
            dispatcher.utter_message("How much money do you have?")
        else:
            dispatcher.utter_message("You have %s rubles and you can buy canned meat" % money)
        return []


class ActionBuyCost(Action):
    def name(self):
        return "action_buy_cost"

    def run(self, dispatcher, tracker, domain):
        money = tracker.get_slot('money')
        if (int(money) >= 10):
            dispatcher.utter_message("Then the bed for the night is yours1.")
        else:
            dispatcher.utter_message("Can not help with this, look elsewhere1.")
        return [SlotSet("money", None)]


class ActionSleep(Action):
    def name(self):
        return "action_sleep"

    def run(self, dispatcher, tracker, domain):
        money = tracker.get_slot('money')
        if (money is None):
            dispatcher.utter_message("Well, how much money do you have?")
        else:
            if (int(money) >= 10):
                dispatcher.utter_message("Then the bed for the night is yours.")
            else:
                dispatcher.utter_message("Can not help with this, look elsewhere.")
            return [SlotSet("money", None)]
        return [SlotSet("money", None)]


class ActionCheck(Action):
    def name(self):
        return "action_check"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("And why are you telling me this?")
        return []
