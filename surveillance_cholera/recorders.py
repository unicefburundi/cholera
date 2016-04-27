from surveillance_cholera.models import CDS, Temporary, Reporter, Patient, Report, TrackPatientMessage
import re
import datetime
import requests
import json
from django.conf import settings


def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	print("==len(args['text'].split(' '))==")
	print(len(args['text'].split(' ')))
	print(args['text'].split(' '))
	if(args['message_type']=='SELF_REGISTRATION'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='PATIENT_REGISTRATION'):
		if len(args['text'].split(' ')) < 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split(' ')) > 6:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split(' ')) == 6:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='TRACK'):
		if len(args['text'].split(' ')) < 4:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split(' ')) > 4:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split(' ')) == 4:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
	if(args['message_type']=='RECEPTION_P_T'):
		if len(args['text'].split(' ')) < 4:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split(' ')) > 4:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split(' ')) == 4:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."




#------------------------------------------------------------------------------------




def check_cds(args):
	''' This function checks if the CDS code sent by the reporter exists '''
	the_cds_code = args['text'].split(' ')[1]
	concerned_cds = CDS.objects.filter(code = the_cds_code)
	if (len(concerned_cds) > 0):
		args['valide'] = True
		args['info_to_contact'] = "Le code cds envoye est reconnu."
	else:
		args['valide'] = False
		args['info_to_contact'] = "Le code cds envoye n est pas enregistre dans le systeme."

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split(' ')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	#expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	expression = r'^(\+?(257)?)((61)|(62)|(68)|(69)|(71)|(72)|(75)|(76)|(79))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Le numero de telephone du superviseur n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

def check_supervisor_phone_number_not_for_this_contact(args):
	'''This function checks if the contact didn't send his/her phone number in the place of the supervisor phone number'''
	print("args['phone']")
	print(args['phone'])
	print("args['phone'][4:]")
	print(args['phone'][4:])
	print("args['text'].split(' ')[2]")
	print(args['text'].split(' ')[2])
	if args['phone'] == args['text'].split(' ')[2] or args['phone'][4:] == args['text'].split(' ')[2]:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero de telephone du superviseur ne peut pas etre le tien."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien note."

def save_temporary_the_reporter(args):
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		same_existing_temp = same_existing_temp[0]
		same_existing_temp.delete()
		args['valide'] = False
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement."
	else:
		the_phone_number = args['phone']

		the_cds_code = args['text'].split(' ')[1]

		cds = CDS.objects.filter(code = the_cds_code)
		if len(cds) > 0:
			the_concerned_cds = cds[0]

			the_supervisor_phone_number = args['text'].split(' ')[2]
			the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")

			if len(the_supervisor_phone_number_no_space) == 8:
				the_supervisor_phone_number_no_space = "+257"+the_supervisor_phone_number_no_space
			if len(the_supervisor_phone_number_no_space) == 11:
				the_supervisor_phone_number_no_space = "+"+the_supervisor_phone_number_no_space

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

	#Let's check if the contact didn't send his/her number in the place of the supervisor number
	check_supervisor_phone_number_not_for_this_contact(args)
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
		#if (the_one_existing_temp.supervisor_phone_number == the_sup_phone_number_without_spaces):
		if (the_sup_phone_number_without_spaces in the_one_existing_temp.supervisor_phone_number) and (len(the_sup_phone_number_without_spaces) >= 8):
			#The confirmation of the phone number of the supervisor pass

			#Let's check if this reporter is not already registered for this CDS
			check_duplication = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds)
			if len(check_duplication) > 0:
				#This reporter is doing registration twice on the same CDS
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre sur ce meme CDS. Merci."
				the_one_existing_temp.delete()
				return
	
			#Let's check if this reporter is not already registered
			check_duplication1 = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number)
			if len(check_duplication1) > 0:
				#This reporter is doing registration twice
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous n avez pas le droit de vous enregistrer plus d une seule fois. Merci."
				the_one_existing_temp.delete()
				return

			Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds,supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)

			the_one_existing_temp.delete()

			args['valide'] = True
			args['info_to_contact'] = "Vous vous etes enregistre correctement."
		else:
			the_one_existing_temp.delete()
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye le numero de telephone du superviseur de differentes manieres."



#-----------------------------------------------------------------

'''def check_patient_id(args):
	 This function checks if the id patient sent is valid.
	The_id_patient = args['text'].split(' ')[1]
	expression = r'^[0-9]+$'
	if len(The_id_patient) > 9:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero du patient envoye est tres long."
		return
	if len(The_id_patient) < 7:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero du patient envoye est tres court."
		return
	if re.search(expression, The_id_patient) is None:
		#The patient id is not well written
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero du patient n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero du patient est bien ecrit."'''

def check_patient_entry_date(args):
	the_entry_date = args['text'].split(' ')[1]
	if len(the_entry_date) < 6:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs pour la date d entree du patient"
		return
	if len(the_entry_date) > 6:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs pour la date d entree du patient"
		return

def check_colline_name(args):
	''' This function checks if the colline name is valid. '''
	print("Will be done after discussions.")

def check_patient_age(args):
	''' This function cheks if the age of the patient is valid. '''
	The_patient_age = args['text'].split(' ')[3]

	#The below list will be putted in localsettings
	valid_ages = ['A1','A2','a1','a2']

	if(The_patient_age not in valid_ages):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee pour age n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee pour age est valide."

def check_gender(args):
	''' This function checks if the value sent for gender is valid. '''
	the_patient_gender = args['text'].split(' ')[4]

	#The bellow list will be putted in localsettings
	gender_values = ['F','M','f','m']

	if(the_patient_gender not in gender_values):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee pour indiquer le genre du patient n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee pour indiquer le genre du patient est valide."

def check_intervention(args):
	''' This function is used to check if the value sent for intervention is valid. '''
	intervention = args['text'].split(' ')[5]
	capitalized_intervention = intervention.title()

	#The bellow list will be putted in localsettings
	interventions_values = ['Hospi','Desh','Pr','Dd']

	if(capitalized_intervention not in interventions_values):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La valeur envoyee pour intervention n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La valeur envoyee pour intervention est valide."

def record_patient(args):
	'''This function is used to record a patient'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the sent patient id is valid
	#check_patient_id(args)
	#if not args['valide']:
	#	return

	#Let's check if the patient entry date is valid
	check_patient_entry_date(args)
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

	#Let's check if the value sent for intervention is valid
	check_intervention(args)
	if not args['valide']:
		return


	#Let's check if the person who sent this message is in the list of reporters
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	one_concerned_cds = one_concerned_reporter.cds

	cds_code = one_concerned_cds.code

	cds_name = one_concerned_cds.name

	#the_time = time.strftime("%Y%m%d")
	#year = the_time[2:4]
	#month = the_time[4:6]
	#day = the_time[6:8]
	#the_reversed_date = day+""+month+""+year

	#The id of a patient is made like this : cds_code+date+patient_number
	#id_patient = cds_code+""+the_reversed_date+""+args['text'].split('+')[1]
	#the reporter sent : date+patient_number.
	id_patient = cds_code+""+args['text'].split(' ')[1]


	#Let's check if the patient with the same id already exists
	patient = Patient.objects.filter(patient_id = id_patient)
	print("len(patient)")
	print(len(patient))
	if len(patient) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Un patient avec cet identifiant existe deja. Veuillez changer l identifiant du patient."
		return


	#Let's work on the entry date of a patient. It's a part of the patient id sent by the reporter.
	entry_date_in_string = args['text'].split(' ')[1][0:6]
	if len(entry_date_in_string) < 6:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye une valeur tres courte pour l identifiant du patient."
		return

	full_entry_date_in_string = entry_date_in_string[0:2]+""+entry_date_in_string[2:4]+"20"+entry_date_in_string[4:6]

	try:
		datetime.datetime.strptime(full_entry_date_in_string, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date d arrivee du patient n est pas valide."
		return

	full_entry_date_in_date = datetime.datetime.strptime(full_entry_date_in_string, "%d%m%Y").date()

	if full_entry_date_in_date > datetime.datetime.now().date():
		#The reporter must not record a partient who haven't yet come
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date d arrivee du patient n est pas valide."
		return

	#Let's check if the entry date is lower than 01/01/2015
	if full_entry_date_in_date < datetime.datetime.strptime("01012015", "%d%m%Y").date():
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date d entree inferieur au 01/01/2015 n est pas permise."
		return


	#====================================Patient is changed how it is==========================================
	#The patient id is now made by two parts.
	#The first part primary key of the cds
	#The second part is number of patient in that cds	

	id_patient = ""

	#The first part of the patient id must have at minimum 3 caracters
	patient_id_1 = str(one_concerned_cds.id)
	if len(patient_id_1) == 1:
		patient_id_1 = "00"+patient_id_1
	if len(patient_id_1) == 2:
		patient_id_1 = "0"+patient_id_1

	#Let's build the second part of the patient id. It made at minimum by 3 caracters
	'''patient_id_2 = str(Report.objects.filter(cds = one_concerned_cds, report_type = args['message_type']).count())
	if len(patient_id_2) == 1:
		patient_id_2 = "00"+patient_id_2
	if len(patient_id_2) == 2:
		patient_id_2 = "0"+patient_id_2'''

	#the_last_patient_at_this_cds = Patient.objects.filter(cds = one_concerned_cds).order_by("-id")[0]
	the_last_patient_at_this_cds = Patient.objects.filter(cds = one_concerned_cds)
	patient_id_2 = '0'
	print("-1-")	
	if(len(the_last_patient_at_this_cds) > 0):
		print("-2-")
		the_last_patient_at_this_cds = Patient.objects.filter(cds = one_concerned_cds).order_by("-id")[0]
		#Let's identify the id used by the system users for this patient
		the_last_patient_id = the_last_patient_at_this_cds.patient_id

		#Let's remove the first part (patient_id_1) and increment the second one
		the_length_of_the_first_part = len(patient_id_1)
		the_second_part = the_last_patient_id[the_length_of_the_first_part:]

		#Let's increment the second part.
		the_second_part_int = int(the_second_part)
		the_second_part_int = the_second_part_int+1

		#patient_id_2 is the second part of the new patient
		patient_id_2 = str(the_second_part_int)
		print("-3-")
	else:
		print("-4-")
		patient_id_2 = '0'

	print("-5-")
	if len(patient_id_2) == 1:
		patient_id_2 = "00"+patient_id_2
	if len(patient_id_2) == 2:
		patient_id_2 = "0"+patient_id_2


	id_patient = patient_id_1+""+patient_id_2

	#Let's check if there is no patient with that id 
	check_patient_exists = Patient.objects.filter(patient_id = id_patient)
	if len(check_patient_exists) > 0:
		args['valide'] = False
		args['info_to_contact'] = "Exception. Consulter l equipe de maintenance du systeme."
		return

	#==========================================================================================================

	#Let's record a patient
	
	#The below line is the best one. The one i activate now is for concordance with A's code.
	#the_created_patient = Patient.objects.create(patient_id = id_patient, colline_name = args['text'].split(' ')[2], age = args['text'].split(' ')[3], sexe = args['text'].split(' ')[4], intervention = args['text'].split(' ')[5], date_entry = full_entry_date_in_date)

	if args['text'].split(' ')[5].title() == 'Dd':
		#This patient is registered as dead. His/Her exit date is his/her entry date
		the_created_patient = Patient.objects.create(patient_id = id_patient, colline_name = args['text'].split(' ')[2].title(), age = args['text'].split(' ')[3].title(), sexe = args['text'].split(' ')[4].title(), intervention = args['text'].split(' ')[5].title(), date_entry = full_entry_date_in_date, cds = one_concerned_cds, exit_date = full_entry_date_in_date, exit_status = 'Pd')

	else:
		the_created_patient = Patient.objects.create(patient_id = id_patient, colline_name = args['text'].split(' ')[2].title(), age = args['text'].split(' ')[3].title(), sexe = args['text'].split(' ')[4].title(), intervention = args['text'].split(' ')[5].title(), date_entry = full_entry_date_in_date, cds = one_concerned_cds)


	#the_created_report = Report.objects.create(patient = the_created_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'].replace("+", " "), report_type = args['message_type'])
	the_created_report = Report.objects.create(patient = the_created_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])

	args['valide'] = True
	args['info_to_contact'] = "Ce patient a ete bien enregistre avec l identifiant : "+id_patient+". Merci."
		




	print("-Ok-")
	#If there is a new patient, the supervisor of the patient need to be informed

	url = 'https://api.rapidpro.io/api/v1/broadcasts.json'
	token = getattr(settings,'TOKEN','')

	message_to_send_if_new_case = "Un nouveau cas de cholera vient d etre signale. Lieu : "+cds_name

	the_supervisor_phone_number = one_concerned_reporter.supervisor_phone_number
	print("the_supervisor_phone_number")
	print(the_supervisor_phone_number)
	if the_supervisor_phone_number == "":
		print("The phone number is not valid.")
	else:
		#Let's inform the supervisor that there is a new case of cholera
		the_supervisor_phone_number = "tel:"+the_supervisor_phone_number
		data = {"urns": [the_supervisor_phone_number],"text": message_to_send_if_new_case}


		#response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data))


	#If there is a new patient, the is a group of persons which need to be informed
	phone_numbers = getattr(settings,'CENTRAL_GROUP','')
	if len(phone_numbers) > 0:
		#These phone numbers are for central group. Let's send a message to them.
		data = {"urns": phone_numbers,"text": message_to_send_if_new_case}
		#data = {"groups": ["CHOLERA_CENTRALE"], "text": "message_to_send_if_new_case"}
		#response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data))
	
#----------------------------------------PATIENT EXIT REPORT MESSAGES-------------------------







'''def check_validity_of_id(args):
	'This function checks if the patient id is known in the system'

	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	one_concerned_cds = one_concerned_reporter.cds

	cds_code = one_concerned_cds.code



	patient_id = cds_code+""+args['text'].split(' ')[1]
	patient = Patient.objects.filter(patient_id = patient_id)
	if len(patient) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Un patient avec cet identifiant n a pas ete enregistre."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Un patient avec cet identifiant existe." '''

def check_validity_of_id(args):
	'''This function checks if the patient id is known in the system'''
	patient_id = args['text'].split(' ')[1]
	patient = Patient.objects.filter(patient_id = patient_id)
	if len(patient) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Il n y a pas de patient avec cet identifiant."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Un patient avec cet identifiant existe."
	

def check_exit_date(args):
	'''This function checks if the exit date is valid.'''

	#expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{2}$'
	if re.search(expression, args['text'].split(' ')[2]) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return
	

	exit_date = args['text'].split(' ')[2][0:2]+"-"+args['text'].split(' ')[2][2:4]+"-20"+args['text'].split(' ')[2][4:]

	exit_date_without_dash = exit_date.replace("-","")
	try:
		datetime.datetime.strptime(exit_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return


	#if datetime.datetime.strptime(args['text'].split(' ')[2], '%d-%m-%Y') > datetime.datetime.now():
	if datetime.datetime.strptime(exit_date, '%d-%m-%Y') > datetime.datetime.now():
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas pas encore arrivee."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La date indiquee est valide."


def patient_exit_status(args):
	'''This function checks if the exit status is valid.'''

	#The below list will be moved to
	exit_status = ['Pd','Pg','Pr']

	if args['text'].split(' ')[3].title() not in exit_status:
		args['valide'] = False
		args['info_to_contact'] = "L etat de sortie indiquee n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "L etat de sortie indiquee est valide."

def record_track_message(args):
	'''This function is used to record a track patient report'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the patient id sent by the reporter exists
	check_validity_of_id(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the exit date is valid
	check_exit_date(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the exit status is valid
	patient_exit_status(args)
	print(args['valide'])
	if not args['valide']:
		return


	#Let's check if the person who sent this message is in the list of reporters
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	one_concerned_cds = one_concerned_reporter.cds

	cds_code = one_concerned_cds.code

	#concerned_patient = Patient.objects.filter(patient_id = cds_code+""+args['text'].split(' ')[1])
	concerned_patient = Patient.objects.filter(patient_id = args['text'].split(' ')[1])

	one_concerned_patient = concerned_patient[0]

	#the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'].replace("+", " "), report_type = args['message_type'])
	#the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])

	#exit_date = datetime.datetime.strptime(args['text'].split('+')[2], '%Y-%m-%d')



	#day_month_year = args['text'].split(' ')[2].split("-")
	day_month_year = args['text'].split(' ')[2][0:2]+"-"+args['text'].split(' ')[2][2:4]+"-20"+args['text'].split(' ')[2][4:]
	#year_month_day = day_month_year[2]+"-"+day_month_year[1]+"-"+day_month_year[0]
	year_month_day = "20"+args['text'].split(' ')[2][4:]+"-"+args['text'].split(' ')[2][2:4]+"-"+args['text'].split(' ')[2][0:2]


	#Let's check if the exit date is not < to the date the patient came in
	if datetime.datetime.strptime(day_month_year, '%d-%m-%Y').date() < one_concerned_patient.date_entry:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee est inferieur a la date d entree du patient."
		return

	#Let's check if this patient is not reported to be exited
	if one_concerned_patient.exit_date:
		#No longer report needed for this patient
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Il n y a plus de rapport possible pour ce patient. On a enregistre sa sortie."
		return


	the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])
		
	

	#Let's update the patient if it is not a trensfert report
	if args['text'].split(' ')[3].title() != "Pr":
		one_concerned_patient.exit_date = year_month_day
		one_concerned_patient.exit_status = args['text'].split(' ')[3].title()
		one_concerned_patient.save()


	TrackPatientMessage.objects.create(exit_date = year_month_day, exit_status = args['text'].split(' ')[3].title(), report = the_created_report)

	args['valide'] = True
	args['info_to_contact'] = "Votre rapport a ete bien enregistre. Merci."









#--------------------------------------RECORD OF A TRANFERED MESSAGE---------------------------------------

def check_reception_date(args):
	'''This function checks if the reception date is valid.'''

	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{2}$'
	if re.search(expression, args['text'].split(' ')[2]) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return
	
	reception_date = args['text'].split(' ')[2][0:2]+"-"+args['text'].split(' ')[2][2:4]+"-20"+args['text'].split(' ')[2][4:]


	#Let's remove dashs
	reception_date_without_dash = reception_date.replace("-","")
	try:
		datetime.datetime.strptime(reception_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date de reception du patient n est pas valide."
		return

	#Let's check if the reception date is not < to the entry date
	patient_id = args['text'].split(' ')[1]
	patient = Patient.objects.filter(patient_id = patient_id)
	
	if len(patient) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Patient non trouve dans le system."
		return
	else:
		patient = patient[0]

	#if the entry date of this patient have been deleted, we can not do the reception record
	if not patient.date_entry:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date d enregistrement de ce patient a ete suprimee. Contacter l administrateur de ce systeme."
		return
	

	if datetime.datetime.strptime(reception_date, '%d-%m-%Y').date() < patient.date_entry:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date de reception du patient est inferieur a sa date d entree dans le systeme."
		return

	if patient.exit_date:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. On a deja enregistre la sortie pour ce patient. Si pas erreur sur l id, informer l administrateur de ce systeme."
		return
	
	#Let's check if the reception date is not a future date
	if datetime.datetime.strptime(reception_date, '%d-%m-%Y') > datetime.datetime.now():
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas pas encore arrivee."
	else:
		args['valide'] = True
		args['info_to_contact'] = "La date indiquee est valide."



def patient_reception_status(args):
	'''This function checks if the reception status is valid.'''

	
	reception_status = ['Hospi','Desh','Pr','Dd']

	if args['text'].split(' ')[3].title() not in reception_status:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. L etat du patient indique n est pas valide."
	else:
		args['valide'] = True
		args['info_to_contact'] = "L etat du patient indique est valide."



def record_patient_reception(args):
	'''This function is used to record a patient at the reception when transfered'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the patient id sent by the reporter exists
	check_validity_of_id(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the reception date is valid
	check_reception_date(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the reception status is valid
	patient_reception_status(args)
	print(args['valide'])
	if not args['valide']:
		return


	#Let's check if the person who sent this message is in the list of reporters
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	one_concerned_cds = one_concerned_reporter.cds

	cds_code = one_concerned_cds.code

	#concerned_patient = Patient.objects.filter(patient_id = cds_code+""+args['text'].split(' ')[1])
	concerned_patient = Patient.objects.filter(patient_id = args['text'].split(' ')[1])

	one_concerned_patient = concerned_patient[0]


	the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])

	args['valide'] = True
	args['info_to_contact'] = "Votre rapport a ete bien enregistre. Merci."
