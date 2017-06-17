import json, re

from django.shortcuts import render
from django.http import JsonResponse

'''
Regexes for capturing words
'''
# e.g. New York, San Francisco
LOCATION_NAMES = "[A-Z]\w*\s[A-Z]\w+"
# e.g. You're, He's
APOSTROPHE = "\w+[']\w+"
# All other words
WORDS = "\w+"

MATCH_REGEX = LOCATION_NAMES + "|" + APOSTROPHE + "|" + WORDS

recipients = {}


def upload_emails(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        for email in data["emails"]:
            word_count = {}

            for word in re.findall(MATCH_REGEX, email["subject"]):
                if not word in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

            for recipient in email["recipients"]:
                if not recipient in recipients:
                    recipients[recipient] = word_count
                else:
                    for word in word_count:
                        if word in recipients[recipient]:
                            recipients[recipient][word] += word_count[word]
                        else:
                            recipients[recipient][word] = word_count[word]

        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)
