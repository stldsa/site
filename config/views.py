from django.shortcuts import redirect

def podcast_redirect(request):
    response = redirect('/')
    return response