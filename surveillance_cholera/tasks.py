from surveillance_cholera.models import Patient, Report
import datetime
from django.shortcuts import render
import requests

def ask_update_on_patient(request):
	''' This function checks if there is no one or more patient(s) reported to be sick and pass three days without any update '''

	the_current_date = datetime.datetime.now().date()

	#Let's do a filter of patients who came on the third day before today.
	filtered_patients = Patient.objects.filter(date_entry=the_current_date - datetime.timedelta(days=3))


	if len(filtered_patients) > 0:
		necessary_data = []

		for patient in filtered_patients:
			#Let's check if we had any update on this patient.
			updates_reports = Report.objects.filter(patient = patient,report_type = 'TRACK')

			if len(updates_reports) == 0:
				#We didn't have any update on this patient
				#Let's identify the phone number of the reporter who registered this patient and ask to him any update on this patient
				the_registration_report = Report.objects.filter(patient = patient)[0]
				the_register = the_registration_report.reporter
				the_reporter_s_phone_number = the_register.phone_number


				an_object = {}
				an_object['patient_id'] = patient.patient_id
				an_object['entry_date'] = patient.date_entry
				an_object['reporter_phone'] = the_reporter_s_phone_number
				short_patient_id = patient.patient_id[6:]
				#an_object['message'] = "Vous n avez donne aucune nouvelle sur le patient "+patient.patient_id
				an_object['message'] = "Vous n avez donne aucune nouvelle sur le patient "+short_patient_id

				necessary_data.append(an_object)
				#r = requests.post("https://api.rapidpro.io/api/v1/broadcasts.json?Authorization: Token c2195bdeeca5819f1ded643f0152c0e8bf9a8474", data={
  #"urns": [
  	#"tel:0000090779"],
  #"text": "My first message" 
#})

	return render(request, 'test_temporary.html',locals())
