# in a temporary urls.py / views.py
from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_migrations(request):
    if request.method == "POST":
        call_command("migrate")
        return HttpResponse("Migrations applied")
    return HttpResponse("Send a POST request to migrate")
