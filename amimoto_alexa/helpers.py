#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helpers for amimoto_alexa
"""

import yaml
import json
import datetime
import time
import boto3
import lamvery
import xml.etree.ElementTree as ET
from debugger import *


def build_session_attributes(session):
    """ initialize session_attributes when passed None """
    if 'attributes' in session.keys():
        if session['attributes']:
            session_attributes = session['attributes']
        else:
            # called from test
            session_attributes = {}
            session_attributes['state'] = 'started'
            session_attributes['accepted_questions'] = []
            session_attributes['rejected_questions'] = []
    else:
        # called from tap
        session_attributes = {}
        session_attributes['state'] = 'started'
        session_attributes['accepted_questions'] = []
        session_attributes['rejected_questions'] = []

    return session_attributes


def gen_twitter_sentence(twitter_id):
    if twitter_id:
        str = '<p>I found your twitter ID, ' + twitter_id + ".</p>"
    else:
        str = ""

    return str


def ssmlnize_sentence(text):
    output = ""
    text = text.strip()
    lines = text.split("\n")
    for line in lines:
        output = output + "<p>" + line + "</p>"
    return output


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    if not reprompt_text:
        reprompt_text = ""
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': remove_ssml_tags(output)
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" + reprompt_text + "</speak>"
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def load_text_from_yaml(title):
    return yaml.load(open('data/text/{card}.yml'.format(card=title)).read())

def remove_ssml_tags(ssml):
    try:
        text = []
        root = ET.fromstring("<xml>" + ssml + "</xml>")

        for x in root.itertext():
            text.append(x.strip())

        retext = filter(lambda s: s != '', text)
        return " ".join(retext)
    except:
        return ssml
