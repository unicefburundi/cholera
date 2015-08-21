from surveillance_cholera.models import CDS, Temporary
import re

def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	if len(args['text'].split('+')) < 3:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye peu de valeurs."
	if len(args['text'].split('+')) > 3:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
	if len(args['text'].split('+')) == 3:
		args['valide'] = "True"
		args['info_to_contact'] = "Le nombre de valeurs envoye est correct."

def check_cds(args):
	''' This function checks if the CDS code sent by the reporter exists '''
	the_cds_code = args['text'].split('+')[1]
	concerned_cds = CDS.objects.filter(code = the_cds_code)
	if (len(concerned_cds) > 0):
		args['valide'] = "True"
		args['info_to_contact'] = "Le code cds envoye est reconnu."
	else:
		args['valide'] = "False"
		args['info_to_contact'] = "Le code cds envoye n est enregistre dans le systeme."

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split('+')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = "False"
		args['info_to_contact'] = "Le numero de telephone du superviseur n est pas bien ecrit."
	else:
		args['valide'] = "True"
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

def save_temporary_the_reporter(args):
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		args['valide'] = "False"
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement."
	else:
		the_phone_number = args['phone']

		the_cds = args['text'].split('+')[1]
	
		the_supervisor_phone_number = args['text'].split('+')[2]
		the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")

		Temporary.objects.create(phone_number = the_phone_number,cds = the_cds,supervisor_phone_number = the_supervisor_phone_number_no_space)

def temporary_record_reporter(args):
	'''This function is used to record temporary a reporter'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	if not args['valide']:
		return
	

	#Let's check if the code of CDS is valid
	check_cds(args)
	if not args['valide']:
		return

	#Let's check is the supervisor phone number is valid
	check_supervisor_phone_number(args)
	if not args['valide']:
		return

	#Let's temporary save the reporter
	save_temporary_the_reporter(args)
	

#-----------------------------------------------------------------

def record_patient(args):
	print("This function is used to record a patient")

def record_track_message(args):
	print("This function is used to record a track message")
