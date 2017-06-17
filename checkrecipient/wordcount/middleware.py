from datetime import datetime
import threading, time

class WordCounterMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.sessions = {}

    def __call__(self, request):

        '''
        In-memory variable data store
        '''
        if "words" not in request.session:
            request.session["words"] = []
        if "recipients" not in request.session:
            request.session["recipients"] = []
        if "counters" not in request.session:
            request.session["counters"] = {}

        response = self.get_response(request)

        req_time = datetime.now()
        self.sessions[request.session.session_key] = req_time
        threading.Thread(target=self.write_to_db, args=(req_time, request.session, )).start()

        return response

    def write_to_db(self, start_time, session):
        time.sleep(10)

        if self.sessions[session.session_key] == start_time:
            print("One thread is working for" + str(session_key))

            # Freeing up the memory
            self.sessions.pop(session.session_key)
