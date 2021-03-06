#!/usr/bin/python
# -*- coding: utf-8 -*-
Planets_List = [ "Mercury", "Venus","Earth", "Mars", "Jupiter", "Saturn",  "Uranus", "Neptune"]

Planets_Description = {"Mercury": "Mercury the smallest planet in our solar system and closest to the Sun, is only slightly larger than Earth's Moon. Mercury is the fastest planet, zipping around the Sun every 88 Earth days.",
"Venus": "Venus spins slowly in the opposite direction from most planets. A thick atmosphere traps heat in a runaway greenhouse effect, making it the hottest planet in our solar system.",
"Earth": "Earth our home planet, is the only place we know of so far that's inhabited by living things. It's also the only planet in our solar system with liquid water on the surface.",
"Mars": "Mars is a dusty, cold, desert world with a very thin atmosphere. There is strong evidence Mars was billions of years ago, wetter and warmer, with a thicker atmosphere.",
"Jupiter": "Jupiter is more than twice as massive than the other planets of our solar system combined. The giant planet's Great Red spot is a centuries-old storm bigger than Earth.",
"Saturn":"Saturn Adorned with a dazzling, complex system of icy rings, Saturn is unique in our solar system. The other giant planets have rings, but none are as spectacular as Saturn's.",
"Uranus": "Uranus the seventh planet from the Sun 4rotates at a nearly 90-degree angle from the plane of its orbit. This unique tilt makes Uranus appear to spin on its side.",
"Neptune": "Neptune the eighth and most distant major planet orbiting our Sun, is dark, cold and whipped by supersonic winds. It was the first planet located through mathematical calculations, rather than by telescope."}

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the Amazing Space facts Alexa Skill. There are eigth planets in our solar system: " + ', '.join(map(str, Planets_List)) + ". "\
    "If you would like to hear more about a particular planet, you could say for example: tell me about Earth?"
    reprompt_MSG = "Do you want to hear more about a particular planet?"
    card_TEXT = "Pick a planet."
    card_TITLE = "Choose a chess planet."
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")

# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "Planets_p":
        return planet_desc(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions
def planet_desc(event):
    name=event['request']['intent']['slots']['Planet']['value']
    planet_list_lower=[w.lower() for w in Planets_List]
    if name.lower() in planet_list_lower:
        reprompt_MSG = "Do you want to hear more about a particular planet?"
        card_TEXT = "You've picked " + name.lower()
        card_TITLE = "You've picked " + name.lower()
        return output_json_builder_with_reprompt_and_card(Planets_Description[name.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't used the full name of a planet. If you have forgotten which planets you can pick say Help."
        reprompt_MSG = "Do you want to hear more about a particular planet?"
        card_TEXT = "Use the full name."
        card_TITLE = "Wrong name."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these planets: " + ', '.join(map(str, Planets_List)) + ". Be sure to use the full name when asking about the planet."
    reprompt_MSG = "Do you want to hear more about a particular planet?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular planet?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)


def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict


def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict


def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = 'Simple'
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict


def response_field_builder_with_reprompt_and_card(
    outputSpeach_text,
    card_text,
    card_title,
    reprompt_text,
    value,
    ):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict


def output_json_builder_with_reprompt_and_card(
    outputSpeach_text,
    card_text,
    card_title,
    reprompt_text,
    value,
    ):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] =   response_field_builder_with_reprompt_and_card(outputSpeach_text,card_text, card_title, reprompt_text, value)
    return response_dict
