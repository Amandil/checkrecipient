from django.shortcuts import render
from django.http import JsonResponse

def upload_emails(request):
    if request.method == 'POST':
        return JsonResponse({}, status=501)
    else:
        return JsonResponse({}, status=400)
