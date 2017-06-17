from datetime import datetime

class WordCounterMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # request.session["last_activity"] = datetime.now()

        '''
        In-memory variable data store
        '''
        if "words" not in request.session:
            request.session["words"] = []
        if "recipients" not in request.session:
            request.session["recipients"] = []
        if "counters" not in request.session:
            request.session["counters"] = {}

        return self.get_response(request)

# Called during request:
# process_request(request)
# process_view(request, view_func, view_args, view_kwargs)
# Called during response:
# process_exception(request, exception) (only if the view raised an exception)
# process_template_response(request, response) (only for template responses)
# process_response(request, response)
