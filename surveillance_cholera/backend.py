from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@json_view
def handel_external_request(request):
	print("You are in the handel_external_request function.")
