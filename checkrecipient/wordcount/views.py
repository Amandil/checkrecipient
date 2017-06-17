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

def upload_emails(request):

    if request.method == 'POST':

        try:
            data = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return JsonResponse({"Invalid JSON"}, status=403)

        for email in data["emails"]:

            # No point processing the same email twice
            if email["timestamp"] not in request.session["emails"]:
                request.session["emails"][email["timestamp"]] = []

                '''
                Counting all words first
                '''
                word_count = {}
                for word in re.findall(MATCH_REGEX, email["subject"]):
                    if not word in request.session["words"]:
                        request.session["words"].append(word)

                    if not word in word_count:
                        word_count[word] = 1
                    else:
                        word_count[word] += 1

                '''
                Going through all recipients
                '''
                unique_recipients = list(set(email["recipients"]))
                for recipient in unique_recipients:
                    '''
                    If reciepient has not been seen before, recording recipient
                    '''
                    if not recipient in request.session["recipients"]:
                        request.session["recipients"].append(recipient)
                    request.session["emails"][email["timestamp"]].append(request.session["recipients"].index(recipient))

                    '''
                    Incrementing word counts for given recipient
                    '''
                    for word in word_count:

                        key = str(request.session["words"].index(word)) + "-" + str(request.session["recipients"].index(recipient))

                        # If word has been used with this recipient before, increment
                        # otherwise, set to word_count
                        if key in request.session["counters"]:
                            request.session["counters"][key] += word_count[word]

                        else:
                            request.session["counters"][key] = word_count[word]

        # Django onlt considers it a change if a new key has been added
        request.session.modified = True

        '''
        Response here just for manual testing
        '''
        return JsonResponse({
            "emails": request.session["emails"],
            "words": request.session["words"],
            "recipients": request.session["recipients"],
            "counters": request.session["counters"],
        }, status=200)
    else:
        return JsonResponse({}, status=400)
