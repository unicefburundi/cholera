from surveillance_cholera.models import CDS, Temporary, Reporter, Patient, Report, TrackPatientMessage
import re
import datetime

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

		the_cds_code = args['text'].split(' ')[1]

		cds = CDS.objects.filter(code = the_cds_code)
		if len(cds) > 0:
			the_concerned_cds = cds[0]

			the_supervisor_phone_number = args['text'].split(' ')[2]
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

			#Let's check if this reporter is not already registered for this CDS
			check_duplication = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds)
			if len(check_duplication) > 0:
				#This reporter is doing registration twice on the same CDS
				args['valide'] = False
				args['info_to_contact'] = "Vous vous etes deja enregistre sur ce meme CDS. Merci."
				the_one_existing_temp.delete()
				return

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
	The_id_patient = args['text'].split(' ')[1]
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
	The_patient_age = args['text'].split(' ')[3]

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
	the_patient_gender = args['text'].split(' ')[4]

	#The bellow list will be putted in localsettings
	gender_values = ['F','M']

	if(the_patient_gender not in gender_values):
		args['valide'] = False
		args['info_to_contact'] = "La valeur envoyee pour indiquer le genre du patient n est pas valide."
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
		args['info_to_contact'] = "La valeur envoyee pour intervention n est pas valide."
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
		args['info_to_contact'] = "Un patient avec cet identifiant existe deja. Veuillez changer l identifiant du patient."
		return


	#Let's work on the entry date of a patient. It's a part of the patient id sent by the reporter.
	entry_date_in_string = args['text'].split(' ')[1][0:6]
	if len(entry_date_in_string) < 6:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye une valeur tres courte pour l identifiant du patient."
		return

	full_entry_date_in_string = entry_date_in_string[0:2]+""+entry_date_in_string[2:4]+"20"+entry_date_in_string[4:6]


	full_entry_date_in_date = datetime.datetime.strptime(full_entry_date_in_string, "%d%m%Y").date()

	if full_entry_date_in_date > datetime.datetime.now().date():
		#The reporter must not record a partient who haven't yet come
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date d arrivee du patient n est pas valide."
		return

	#Let's record a patient
	
	#The below line is the best one. The one i activate now is for concordance with A's code.
	#the_created_patient = Patient.objects.create(patient_id = id_patient, colline_name = args['text'].split(' ')[2], age = args['text'].split(' ')[3], sexe = args['text'].split(' ')[4], intervention = args['text'].split(' ')[5], date_entry = full_entry_date_in_date)


	the_created_patient = Patient.objects.create(patient_id = id_patient, colline_name = args['text'].split(' ')[2], age = args['text'].split(' ')[3], sexe = args['text'].split(' ')[4], intervention = args['text'].split(' ')[5], date_entry = full_entry_date_in_date, cds = one_concerned_cds)


	#the_created_report = Report.objects.create(patient = the_created_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'].replace("+", " "), report_type = args['message_type'])
	the_created_report = Report.objects.create(patient = the_created_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])

	args['valide'] = True
	args['info_to_contact'] = "Ce patient a ete bien enregistre avec l identifiant : "+id_patient+". Merci."
#-----------------------------------------------------------------
def check_validity_of_id(args):
	'''This function checks if the patient id is known in the system'''

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
		args['info_to_contact'] = "Un patient avec cet identifiant existe."

def check_exit_date(args):
	'''This function checks if the exit date is valid.'''

	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
	if re.search(expression, args['text'].split(' ')[2]) is None:
		args['valide'] = False
		args['info_to_contact'] = "La date indiquee n est pas valide."
		return

	if datetime.datetime.strptime(args['text'].split(' ')[2], '%d-%m-%Y') > datetime.datetime.now():
		args['valide'] = False
		args['info_to_contact'] = "La date indiquee n est pas valide."
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
		args['info_to_contact'] = "Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]

	one_concerned_cds = one_concerned_reporter.cds

	cds_code = one_concerned_cds.code

	concerned_patient = Patient.objects.filter(patient_id = cds_code+""+args['text'].split(' ')[1])

	one_concerned_patient = concerned_patient[0]

	#the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'].replace("+", " "), report_type = args['message_type'])
	the_created_report = Report.objects.create(patient = one_concerned_patient, reporter = one_concerned_reporter, cds = one_concerned_cds, message = args['text'], report_type = args['message_type'])

	#exit_date = datetime.datetime.strptime(args['text'].split('+')[2], '%Y-%m-%d')



	day_month_year = args['text'].split(' ')[2].split("-")
	year_month_day = day_month_year[2]+"-"+day_month_year[1]+"-"+day_month_year[0]

	TrackPatientMessage.objects.create(exit_date = year_month_day, exit_status = args['text'].split(' ')[3], report = the_created_report)

	args['valide'] = True
	args['info_to_contact'] = "Votre rapport a ete bien enregistre. Merci."



