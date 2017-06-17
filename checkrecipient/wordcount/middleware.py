from datetime import datetime
import threading, time

from django.db import transaction
from django.db.models import F

from .models import Email, Recipient, Word
DELAY_SECONDS = 2

class WordCounterMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.sessions = {}

    def __call__(self, request):

        # If last session activity was too long ago, clear the session
        if "last_activity" in request.session:
            last_activity = datetime.strptime(request.session["last_activity"], "%Y-%m-%d %H:%M:%S.%f")
            time_difference = datetime.now() - last_activity
            if time_difference.seconds >= DELAY_SECONDS - 1:
                request.session["emails"] = {}
                request.session["words"] = []
                request.session["recipients"] = []
                request.session["counters"] = {}

        request.session["last_activity"] = str(datetime.now())


        '''
        In-memory variable data store
        '''
        if "emails" not in request.session:
            request.session["emails"] = {}
        if "words" not in request.session:
            request.session["words"] = []
        if "recipients" not in request.session:
            request.session["recipients"] = []
        if "counters" not in request.session:
            request.session["counters"] = {}

        response = self.get_response(request)

        if request.session.session_key is not None:
            self.sessions[request.session.session_key] = request.session["last_activity"]
            threading.Thread(target=self.write_to_db, args=(request.session, )).start()

        return response

    def write_to_db(self, session):
        time.sleep(DELAY_SECONDS)

        if self.sessions[session.session_key] == session["last_activity"]:

            with transaction.atomic():

                # Recording emails and recipients
                for email_timestamp in session["emails"]:
                    db_email = Email(timestamp=email_timestamp)
                    db_email.save()

                    for recipient_index in session["emails"][email_timestamp]:
                        db_recipient = Recipient(email=db_email, address=session["recipients"][recipient_index])
                        db_recipient.save()

                for counter in session["counters"]:
                    parts = counter.split('-')
                    word_index = int(parts[0])
                    word = session["words"][word_index]
                    address_index = int(parts[1])
                    address = session["recipients"][address_index]

                    (new_word, created) = Word.objects.get_or_create(address=address, word=word)
                    if created:
                        new_word.count = session["counters"][counter]
                    else:
                        new_word.count = F('count') + session["counters"][counter]
                    new_word.save()

            # Freeing up the memory
            self.sessions.pop(session.session_key)
