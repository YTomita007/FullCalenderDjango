from django.template import loader
from django.http import HttpResponse
from django.middleware.csrf import get_token

def index(request):
    # CSRFのトークンを発行する
    get_token(request)

    template = loader.get_template("rocket.html")
    return HttpResponse(template.render())
