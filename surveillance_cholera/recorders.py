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
	

def check_supervisor_phone_number(args):
	pass

def save_temporary_the_reporter(args):
	pass

def temporary_record_reporter(args):
	'''This function is used to record temporary a reporter'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	if not args['valide']:
		return
	

	#Let's check if the code of CDS is valid
	check_cds(args)

	#Let's check is the supervisor phone number is valid
	check_supervisor_phone_number(args)

	#Let's temporary save the reporter
	save_temporary_the_reporter(args)
	

def record_patient(args):
	print("This function is used to record a patient")

def record_track_message(args):
	print("This function is used to record a track message")
