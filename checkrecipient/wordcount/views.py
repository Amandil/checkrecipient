from django.shortcuts import render
from django.http import JsonResponse

def upload_emails(request):
    if request.method == 'POST':
        pass
    else:
        return JsonResponse({}, status=400)
