from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@json_view
def handel_rapidpro_request(request):
	'''This function receives requests sent by RapidPro.
	This function send json data to RapidPro as a response.'''

	#We will put all data sent by RapidPro in this variable
	incoming_data = {}

	#Two couples of variable/value are separated by &
	#Let's put couples of variable/value in a list called 'list_of_data'
	list_of_data = request.body.split("&")

	#Let's put all the incoming data in the dictionary 'incoming_data'
	for couple in list_of_data:
		incoming_data[couple.split("=")[0]] = couple.split("=")[1]
