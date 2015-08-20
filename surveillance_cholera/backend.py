from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import urllib2
from django.conf import settings
from surveillance_cholera.models import Reporter, Session
import re


def identify_message(args):
	''' This function identifies which kind of message this message is. '''

	if args['text'].split('+')[0] in getattr(settings,'KNOWN_PREFIXES',''):
		#Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
		args['message_type'] = getattr(settings,'KNOWN_PREFIXES','')[args['text'].split('+')[0]]
	else:
		args['message_type'] = "UNKNOWN_MESSAGE"
		
def check_session(args):
	'''This function checks if there is an already created session'''
	reporter_phone_number = args['phone']
	concerned_reporter = Reporter.objects.filter(phone_number = reporter_phone_number)
	if len(concerned_reporter) < 1:
		args['has_session'] = False
	else:
		args['has_session'] = True

def complete_registration(args):
	'''This function complete a registration of a reporter'''
	print("Put here some code.")

def eliminate_unnecessary_spaces(args):
	'''This function eliminate unnecessary spaces in an the incoming message'''
	the_incoming_message = args['text']
	the_new_message = re.sub(' +',' ',the_incoming_message)
	args['text'] = the_new_message

def record_reporter(args):
	'''This function record a contact'''
	phone_number = args['phone']

def record_patient(args):
	pass

def record_track_message():
	pass
	

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

	#Let's assume that the incoming data is valide
	incoming_data['valide'] = True
	incoming_data['info'] = "The default information."
	

	#Let's instantiate the variable this function will return
	response = {}


	#Let's eliminate unnecessary spaces in the incoming message
	eliminate_unnecessary_spaces(incoming_data)


	#Let's check which kind of message this message is.
	identify_message(incoming_data)
	if(incoming_data['message_type']=='UNKNOWN_MESSAGE'):
		#Let's check if this contact is confirming his phone number
		#It means that he has an already created session
		check_session(incoming_data)
		if not(incoming_data['has_session']):
			#This contact doesn't have an already created session
			response['ok'] = False
			response['info_to_contact'] = "Nous n'avons pas compris votre message."
			return response
		else:
			#This contact is confirming the phone number of his supervisor
			complete_registration(incoming_data)
			return response
	
	
	if(incoming_data['message_type']=='SELF_REGISTRATION'):
			#The contact who sent the current message is doing self registration  in the group of reporters
			record_reporter(incoming_data)
	if(incoming_data['message_type']=='PATIENT_REGISTRATION'):
			#The contact who sent the current message is registering a patient
			record_patient(incoming_data)
	if(incoming_data['message_type']=='TRACK'):
			#The contact who sent the current message is sending a patient track message
			record_track_message(incoming_data)

	if incoming_data['valide'] :
		#The message have been recorded
		response['ok'] = True
	else:
		#The message haven't been recorded
		response['ok'] = False

	response['info_to_contact'] = incoming_data['info_to_contact']



	return response
	
