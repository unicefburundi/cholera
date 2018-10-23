from surveillance_cholera.models import Patient, Report
import datetime
from django.shortcuts import render
import requests
from json2xls import Json2Xls
import json
from django.conf import settings


def ask_update_on_patient(request):
    """ This function checks if there is no one or more patient(s) reported to be sick and pass three days without any update """
    # token = raw_input('Enter your token: ')

    token = getattr(settings, "TOKEN", "")
    if not token:
        print ("...token...")
        print (token)
        return render(request, "test_temporary.html", locals())

    contacts_url = "https://api.rapidpro.io/api/v1/broadcasts.json"

    the_current_date = datetime.datetime.now().date()

    # Let's do a filter of patients who came on the third day before today.
    # filtered_patients = Patient.objects.filter(date_entry=the_current_date - datetime.timedelta(days=3))
    filtered_patients = Patient.objects.filter(
        date_entry__lte=the_current_date - datetime.timedelta(days=3),
        exit_date__isnull=True,
    )

    if len(filtered_patients) > 0:
        necessary_data = []
        for patient in filtered_patients:
            # Let's check if the patient has a corresponding report
            correspond_report = Report.objects.filter(patient=patient)
            if len(correspond_report) > 0:
                # Let's check if we had any update on this patient.
                updates_reports = Report.objects.filter(
                    patient=patient, report_type="TRACK"
                )

                if len(updates_reports) == 0 and patient.intervention != "Dd":
                    # We didn't have any update on this patient
                    # Let's identify the phone number of the reporter who registered this patient and ask to him any update on this patient
                    the_registration_report = Report.objects.filter(patient=patient)[0]
                    the_register = the_registration_report.reporter
                    the_reporter_s_phone_number = the_register.phone_number

                    an_object = {}
                    an_object["patient_id"] = patient.patient_id
                    an_object["entry_date"] = patient.date_entry
                    an_object["reporter_phone"] = the_reporter_s_phone_number
                    an_object["supervisor_phone"] = the_register.supervisor_phone_number
                    # short_patient_id = patient.patient_id[6:]
                    # short_patient_id = patient.patient_id[5:]
                    # an_object['message'] = "Vous n avez donne aucune nouvelle sur le patient "+patient.patient_id
                    # an_object['message'] = "Vous n avez donne aucune nouvelle sur le patient "+short_patient_id
                    an_object["message"] = (
                        "Il y a plus de 3 jours sans nouvelles sur le patient "
                        + an_object["patient_id"]
                        + " enregistre par "
                        + an_object["reporter_phone"]
                        + " sur le CDS dont le code est "
                        + the_registration_report.cds.code
                        + "."
                    )

                    necessary_data.append(an_object)

                    if the_register.supervisor_phone_number:
                        if the_register.supervisor_phone_number.startswith("+257"):
                            sup_phone_number = (
                                "tel:" + the_register.supervisor_phone_number
                            )
                        else:
                            sup_phone_number = (
                                "tel:+257" + the_register.supervisor_phone_number
                            )
                        print (sup_phone_number)
                        print (sup_phone_number)
                        # the_message_to_send = "Vous n avez donne aucune nouvelle sur le patient "+short_patient_id
                        the_message_to_send = an_object["message"]
                        data = {"urns": [sup_phone_number], "text": the_message_to_send}
                        response = requests.post(
                            contacts_url,
                            headers={
                                "Content-type": "application/json",
                                "Authorization": "Token %s" % token,
                            },
                            data=json.dumps(data),
                        )
                        print response.content

                    # r = requests.post("https://api.rapidpro.io/api/v1/broadcasts.json?Authorization: Token c2195bdeeca5819f1ded643f0152c0e8bf9a8474", data={
                    # "urns": [
                    # "tel:0000090779"],
                    # "text": "My first message"
                    # })

    return render(request, "test_temporary.html", locals())
