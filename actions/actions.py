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
from rasa_core_sdk.events import AllSlotsReset
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

class StalkerAnecdote(Action):
    """
    It responds with certain anecdote by elasticsearch query, if theme was specified properly, or throws random joke

    """

    def name(self):
        return 'tell_an_anecdote'

    def run(self, dispatcher, tracker, domain):
        theme = tracker.get_slot('anecdote_theme')
        es = Elasticsearch()

        buttons = []
        laugh = "a"
        for i in range(3):
            laugh = laugh + "ha"
            payload = "/laugh"
            buttons.append({"title": laugh, "payload": payload})

        #empty theme slot --> random joke
        if(theme is None):
            dispatcher.utter_message('Attention, anecdote!')
            dispatcher.utter_button_template('utter_joke', buttons, tracker)
        else:
            anecdotes = es.search(index='jokes', body={"query":{"match":{"anecdote": theme}}})['hits']['hits']
            if anecdotes:
                #for i in anecdotes:
                #    dispatcher.utter_message(i['_source']['anecdote'])
                dispatcher.utter_message(random.choice(anecdotes)['_source']['anecdote'])
                dispatcher.utter_button_template('utter_laugh', buttons, tracker)
            else:
                #elastic return empty answer --> random joke
                dispatcher.utter_message('There should be funny anecdote with ' + theme)
                dispatcher.utter_message('But i don\'t know any, so take this instead')
                dispatcher.utter_button_template('utter_joke', buttons, tracker)
        return [SlotSet('anecdote_theme', None)]

class AnswerQuestion(Action):
    def name(self):
        return "answer_question"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        info = tracker.get_slot('info')
        if(info is None):
            dispatcher.utter_message("I don't know what are you talking about. Try again.")
        else:
            es = Elasticsearch()
            res = es.search(index="desc", body = {"query": {"match":{'title': info}}})
            if(res['hits']['total']['value'] == 0):
                dispatcher.utter_message("I don't know about that thing. May be it has different name. Try again.")
            else:
                dispatcher.utter_message("Yea, I can tell you a lot of things about %s" % info)
                for item in res['hits']['hits']:
                    dispatcher.utter_message(item['_source']['description'])
        return [SlotSet('info', None)]


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


class ActionHurryUp(Action):
    def name(self):
        return "action_hurry_up"

    def run(self, dispatcher, tracker, domain):
        time_till_emission = 60 - datetime.datetime.today().minute
        dispatcher.utter_template("utter_hurry_up", tracker, time_till_emission=time_till_emission)
        return []


class ActionCheckHideaway(Action):
    def name(self):
        return "action_check_hideaway"

    def run(self, dispatcher, tracker, domain):
        connection = MongoClient("ds127376.mlab.com", 27376)
        db = connection["chatbot"]
        db.authenticate("rasaguy", "rasabot1")
        collection = db['stations']
        stations = [document['station_name'].lower() for document in collection.find()]
        connection.close()

        station_name = tracker.get_slot('station_name')
        station_name = station_name.lower() if station_name else None

        if station_name is None:
            dispatcher.utter_template("utter_dont_know_place", tracker)
            return [SlotSet("station_name", None)]

        if station_name not in stations:
            for true_station in stations:
                n_diffs = sum(1 for a, b in zip(station_name, true_station) if a != b)
                if n_diffs == 1:
                    time_till_emission = 60 - datetime.datetime.today().minute
                    dispatcher.utter_message(
                        "Maybe you mean {}. Then you should hurry because emission will be in {} minutes".format(
                            true_station, time_till_emission))
                    return [SlotSet("station_name", None)]
            dispatcher.utter_template("utter_dont_know_place", tracker)
            return [SlotSet("station_name", None)]

        is_can = random.choice([True, False])
        if is_can:
            dispatcher.utter_template("utter_can_hide", tracker)
            time_till_emission = 60 - datetime.datetime.today().minute
            if time_till_emission < 20:
                dispatcher.utter_template("utter_hurry_up", tracker, time_till_emission=time_till_emission)
        else:
            dispatcher.utter_template("utter_cant_hide", tracker)

        return [SlotSet("station_name", None)]


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
        time_till_emission = 60 - datetime.datetime.today().minute
        if time_till_emission < 20:
            dispatcher.utter_message("Hurry up! The emission will be in {}".format(time_till_emission))
        else:
            dispatcher.utter_message("You have enough time. The emission will be in {} minutes".format(time_till_emission))
        return []


class ActionBuy(Action):
    def name(self):
        return "action_buy"

    def run(self, dispatcher, tracker, domain):
        money = tracker.get_slot('money')
        food = [["bread", 5], ["canned food", 15], ["sausage", 25], ["vodka", 35], ["energy drink", 45]]
        if money is None:
            t = ""
            for i in range(len(food)):
                if i > 0:
                    t += ", "
                t += food[i][0]
            dispatcher.utter_message("What would you like to buy? I have %s." % t)
        else:
            t = ""
            for i in range(len(food)):
                if int(money) >= food[i][1]:
                    if i > 0:
                        t += ", "
                    t += food[i][0]
            if t is "":
                dispatcher.utter_message("You don't have enough")
            else:
                dispatcher.utter_message("With this money you can buy %s. What will you choose?" % t)
        return []


class ActionFoodSelect(Action):
    def name(self):
        return "action_food_select"

    def run(self, dispatcher, tracker, domain):
        item = tracker.get_slot('purchased_item')
        money = tracker.get_slot('money')
        if money is None:
            if item is None:
                dispatcher.utter_message("I don't understand, can you repeat?")
            else:
                dispatcher.utter_message("If you want %s, tell me how much money will you give?" % item)
        else:
            food = {"bread": 5, "canned food": 15, "sausage": 25, "vodka": 35, "energy drink": 45}
            d = food.get(item)
            if d is None:
                dispatcher.utter_message("This is not available.")
            else:
                if int(money) >= food[item]:
                    dispatcher.utter_message("Take it.")
                else:
                    dispatcher.utter_message("You don't have enough. It costs at least %s rubles." % food[item])
        return [SlotSet("money", None)]


class ActionBuyCost(Action):
    def name(self):
        return "action_buy_cost"

    def run(self, dispatcher, tracker, domain):
        money = tracker.get_slot('money')
        if int(money) >= 10:
            dispatcher.utter_message("Then the bed for the night is yours.")
        else:
            dispatcher.utter_message("Can not help with this, look elsewhere.")
        return [SlotSet("money", None)]


class ActionSleep(Action):
    def name(self):
        return "action_sleep"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Well, how much money do you have?")
        return [SlotSet("money", None)]


class ActionCheck(Action):
    def name(self):
        return "action_check"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("And why are you telling me this?")
        return []


class Bye(Action):
    def name(self):
        return "action_goodbye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_goodbye', tracker)
        return [AllSlotsReset()]
