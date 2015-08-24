from surveillance_cholera.models import CDS, Temporary, Reporter
import re

def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	if(args['message_type']=='SELF_REGISTRATION'):
		if len(args['text'].split('+')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split('+')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split('+')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(incoming_data['message_type']=='PATIENT_REGISTRATION'):
		if len(args['text'].split('+')) < 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split('+')) > 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split('+')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."




#------------------------------------------------------------------------------------




def check_cds(args):
	''' This function checks if the CDS code sent by the reporter exists '''
	the_cds_code = args['text'].split('+')[1]
	concerned_cds = CDS.objects.filter(code = the_cds_code)
	if (len(concerned_cds) > 0):
		args['valide'] = True
		args['info_to_contact'] = "Le code cds envoye est reconnu."
	else:
		args['valide'] = False
		args['info_to_contact'] = "Le code cds envoye n est enregistre dans le systeme."

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split('+')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Le numero de telephone du superviseur n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

def save_temporary_the_reporter(args):
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement."
	else:
		the_phone_number = args['phone']

		the_cds_code = args['text'].split('+')[1]

		cds = CDS.objects.filter(code = the_cds_code)
		if len(cds) > 0:
			the_concerned_cds = cds[0]

			the_supervisor_phone_number = args['text'].split('+')[2]
			the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")

			Temporary.objects.create(phone_number = the_phone_number,cds = the_concerned_cds,supervisor_phone_number = the_supervisor_phone_number_no_space)
			args['valide'] = True
			args['info_to_contact'] = "Merci. Veuillez confirmer le numero du superviseur s il vous plait."

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
	

def complete_registration(args):
	the_sup_phone_number = args['text']
	the_sup_phone_number_without_spaces = the_sup_phone_number.replace(" ", "")

	the_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	
	if len(the_existing_temp) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Votre message n est pas considere."
	else:
		the_one_existing_temp = the_existing_temp[0]
		if (the_one_existing_temp.supervisor_phone_number == the_sup_phone_number_without_spaces):
			#The confirmation of the phone number of the supervisor pass
			Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds,supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)

			the_one_existing_temp.delete()

			args['valide'] = True
			args['info_to_contact'] = "Vous vous etes enregistre correctement."
		else:
			the_one_existing_temp.delete()
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye le numero de telephone du superviseur de differentes manieres. Recommencer l enregistrement."



#-----------------------------------------------------------------

def check_patient_id(args):
	''' This function checks if the id patient sent is valid. '''
	The_id_patient = args['text'].split('+')[1]
	expression = r'^[0-9]+$'
	if re.search(expression, The_id_patient) is None:
		#The patient id is not well written
		args['valide'] = False
		args['info_to_contact'] = "Le numero du patient n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero du patient est bien ecrit."	

def check_colline_name(args):
	''' This function checks if the colline name is valid. '''
	print("Will be done after discussions.")

def check_patient_age(args):
	''' This function cheks if the age of the patient is valid. '''
	The_patient_age = args['text'].split('+')[3]
	
	#The below list will be putted in localsettings
	valid_ages = ['A1','A2']

	if(The_patient_age not in valid_ages):
		args['valide'] = False
		args['info_to_contact'] = "La valeur envoyee pour age n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee pour age est valide."

def check_gender(args):
	''' This function checks if the value sent for gender is valid. '''
	the_patient_gender = args['text'].split('+')[4]
	
	#The bellow list will be putted in localsettings
	gender_values = ['F','M']

	if(the_patient_gender not in gender_values):
		args['valide'] = False
		args['info_to_contact'] = "La valeur envoyee pour indiquer le genre du patient n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee pour indiquer le genre du patient est valide."

def record_patient(args):
	'''This function is used to record a patient'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	if not args['valide']:
		return

	#Let's check if the sent patient id is valid
	check_patient_id(args)
	if not args['valide']:
		return

	#Let's check if the colline name is valid
	check_colline_name(args)
	if not args['valide']:
		return

	#Let's check if the age of the patient is valid
	check_patient_age(args)
	if not args['valide']:
		return

	#Let's check if the value sent for gender id valid
	check_gender(args)
	if not args['valide']:
		return
	
#-----------------------------------------------------------------
def record_track_message(args):
	print("This function is used to record a track message")
