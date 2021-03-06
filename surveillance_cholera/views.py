from django.views.generic import ListView, DetailView, CreateView, UpdateView
from surveillance_cholera.models import *
from django_tables2 import RequestConfig
from surveillance_cholera.tables import PatientsTable, Patients2Table
from django.shortcuts import render
from surveillance_cholera.forms import (
    PatientSearchForm,
    SearchForm,
    AlertForm,
    CDSForm,
    DistrictForm,
    ProvinceForm,
)
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable, ReportTable
from cholera.views import get_all_patients
from django.db.models import Q
import datetime
from django.views.generic import FormView
from surveillance_cholera.templatetags.extras_utils import *
import operator
from surveillance_cholera.forms import UserCreationMultiForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordResetForm

###########
# CDS             ##
###########


def get_per_cds_statistics(moh_facility_id, start_date="", end_date=""):
    if not start_date:
        start_date = datetime.date(2015, 1, 1).strftime("%Y-%m-%d")
    if end_date:
        end_date = datetime.date.today().strftime("%d/%m/%Y")
    patients = Patient.objects.filter(
        date_entry__range=[format_to_time(start_date), format_to_time(end_date)]
    ).filter(cds=moh_facility_id)
    cds_id = {"cds_id": CDS.objects.get(id=moh_facility_id).id}
    facility = {"name": CDS.objects.get(id=moh_facility_id).name}
    detail = {"detail": CDS.objects.get(id=moh_facility_id).code}
    total = {"total": Patient.objects.filter(cds=moh_facility_id).count()}
    deces = {
        "deces": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in DEAD
            ),
        ).count()
    }
    hospi = {
        "hospi": reduce(
            operator.or_,
            (patients.filter(intervention__icontains=item) for item in HOSPI),
        ).count()
    }
    new_cases = {"new_cases": patients.count()}
    gueris = {
        "gueris": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in GUERI
            ),
        ).count()
    }
    references = {
        "references": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in REFER
            ),
        ).count()
    }

    elemet = {}
    for i in [
        total,
        deces,
        hospi,
        new_cases,
        references,
        gueris,
        facility,
        detail,
        cds_id,
    ]:
        elemet.update(i)
    return elemet


class CDSCreateView(CreateView):
    model = CDS
    form_class = CDSForm


class CDSListView(ListView):
    model = CDS
    paginate_by = 25


class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, *args, **kwargs):
        context = super(CDSDetailView, self).get_context_data(*args, **kwargs)
        cds_id = self.kwargs["pk"]
        data = None
        if "sstart_date" in self.request.session:
            data = [
                get_per_cds_statistics(
                    cds_id,
                    start_date=self.request.session["sstart_date"],
                    end_date=self.request.session["eend_date"],
                )
            ]
            context["start_date"] = self.request.session["sstart_date"]
            context["end_date"] = self.request.session["eend_date"]
        else:
            data = [get_per_cds_statistics(cds_id)]
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context["statistics"] = statistics
        context["form"] = SearchForm()
        return context


class CDSFormView(FormView, CDSDetailView):
    models = CDS
    form_class = SearchForm
    template_name = "surveillance_cholera/cds_detail.html"

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = [
            get_per_cds_statistics(
                kwargs["pk"],
                request.POST.get("start_date"),
                request.POST.get("end_date"),
            )
        ]
        statistics = PatientsTable(data)
        RequestConfig(request).configure(statistics)
        request.session["sstart_date"] = request.POST.get("start_date")
        request.session["eend_date"] = request.POST.get("end_date")

        return render(
            request,
            "surveillance_cholera/cds_detail.html",
            {
                "form": form,
                "statistics": statistics,
                "object": CDS.objects.get(pk=kwargs["pk"]),
                "start_date": request.POST.get("start_date"),
                "end_date": request.POST.get("end_date"),
            },
        )


###########
# District        ##
###########


def get_per_district_statistics(moh_facility_id, start_date="", end_date=""):
    if not start_date:
        start_date = u"01/01/2015"
    if not end_date:
        end_date = datetime.date.today().strftime("%d/%m/%Y")
    patients = Patient.objects.filter(
        date_entry__range=[format_to_time(start_date), format_to_time(end_date)]
    ).filter(cds__district=moh_facility_id)
    district_id = {"district_id": District.objects.get(id=moh_facility_id).id}
    facility = {"name": District.objects.get(id=moh_facility_id).name}
    detail = {"detail": District.objects.get(id=moh_facility_id).id}
    total = {"total": Patient.objects.filter(cds__district=moh_facility_id).count()}
    deces = {
        "deces": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in DEAD
            ),
        ).count()
    }
    hospi = {
        "hospi": reduce(
            operator.or_,
            (patients.filter(intervention__icontains=item) for item in HOSPI),
        ).count()
    }
    new_cases = {"new_cases": patients.count()}
    gueris = {
        "gueris": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in GUERI
            ),
        ).count()
    }
    references = {
        "references": reduce(
            operator.or_,
            (
                patients.filter(
                    Q(intervention__icontains=item) | Q(exit_status__icontains=item)
                )
                for item in REFER
            ),
        ).count()
    }

    elemet = {}
    for i in [
        total,
        deces,
        hospi,
        new_cases,
        facility,
        references,
        gueris,
        detail,
        district_id,
    ]:
        elemet.update(i)
    return elemet


def get_district_data(moh_facility_id, start_date="", end_date=""):
    elemet = []
    for i in CDS.objects.filter(district=moh_facility_id):
        elemet.append(get_per_cds_statistics(i.id, start_date, end_date))
    return elemet


class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm


class DistrictListView(ListView):
    model = District
    paginate_by = 25


class DistrictDetailView(DetailView):
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        district_id = self.kwargs["pk"]
        data = None
        if "sstart_date" in self.request.session:
            data = get_district_data(
                district_id,
                start_date=self.request.session["sstart_date"],
                end_date=self.request.session["eend_date"],
            )
            context["start_date"] = self.request.session["sstart_date"]
            context["end_date"] = self.request.session["eend_date"]
        else:
            data = get_district_data(district_id)
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context["statistics"] = statistics
        context["form"] = SearchForm()
        return context


class DistrictFormView(FormView, DistrictDetailView):
    models = District
    form_class = SearchForm
    template_name = "surveillance_cholera/district_detail.html"

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = get_district_data(
            kwargs["pk"], request.POST.get("start_date"), request.POST.get("end_date")
        )
        statistics = PatientsTable(data)
        RequestConfig(request).configure(statistics)
        request.session["sstart_date"] = request.POST.get("start_date")
        request.session["eend_date"] = request.POST.get("end_date")

        return render(
            request,
            "surveillance_cholera/district_detail.html",
            {
                "form": form,
                "statistics": statistics,
                "object": District.objects.get(pk=kwargs["pk"]),
                "start_date": request.POST.get("start_date"),
                "end_date": request.POST.get("end_date"),
            },
        )


###########
# Province      ##
###########


def get_province_data(moh_facility_id, start_date="", end_date=""):
    elemet = []
    for i in District.objects.filter(province=moh_facility_id):
        elemet.append(get_per_district_statistics(i.id, start_date, end_date))
    return elemet


class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm


class ProvinceListView(ListView):
    model = Province
    paginate_by = 50


class ProvinceDetailView(DetailView):
    model = Province

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        province_id = self.kwargs["pk"]
        data = None
        # import ipdb; ipdb.set_trace()
        if "sstart_date" in self.request.session:
            data = get_province_data(
                province_id,
                start_date=self.request.session["sstart_date"],
                end_date=self.request.session["eend_date"],
            )
            context["start_date"] = self.request.session["sstart_date"]
            context["end_date"] = self.request.session["eend_date"]
        else:
            data = get_province_data(province_id)

        statistics = Patients2Table(data)
        RequestConfig(self.request, paginate={"per_page": 1000}).configure(statistics)
        context["statistics"] = statistics
        context["form"] = SearchForm()
        return context


class ProvinceFormView(FormView, ProvinceDetailView):
    models = Province
    form_class = SearchForm
    template_name = "surveillance_cholera/province_detail.html"

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = get_province_data(
            kwargs["pk"], request.POST.get("start_date"), request.POST.get("end_date")
        )
        statistics = Patients2Table(data)
        RequestConfig(request, paginate={"per_page": 1000}).configure(statistics)
        request.session["sstart_date"] = request.POST.get("start_date")
        request.session["eend_date"] = request.POST.get("end_date")

        return render(
            request,
            "surveillance_cholera/province_detail.html",
            {
                "form": form,
                "statistics": statistics,
                "object": Province.objects.get(pk=kwargs["pk"]),
                "start_date": request.POST.get("start_date"),
                "end_date": request.POST.get("end_date"),
            },
        )


###########
# Patient        ##
###########


class PatientListView(ListView):
    model = Patient
    paginate_by = 50

    def get_queryset(self):
        qs = Patient.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == "CDS":
            qs = Patient.objects.filter(cds__code=int(user.moh_facility))
        if user.level == "BDS":
            qs = Patient.objects.filter(cds__district__code=int(user.moh_facility))
        if user.level == "BPS":
            qs = Patient.objects.filter(
                cds__district__province__code=int(user.moh_facility)
            )
        return qs


class PatientDetailView(DetailView):
    model = Patient

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        patient_id = self.kwargs["pk"]
        data = Report.objects.filter(patient__id=patient_id)
        reports = ReportTable(data)
        RequestConfig(self.request, paginate={"per_page": 1000}).configure(reports)
        context["reports"] = reports
        return context


@login_required
def get_patients_by_code(request, code=""):
    userprofile = UserProfile.objects.get(user=request.user)
    all_patients = get_all_patients(
        level=userprofile.level, moh_facility=userprofile.moh_facility
    )
    form = PatientSearchForm()
    moh_facility = None
    if 1 <= len(code) <= 2:
        moh_facility = Province.objects.get(code=code)
        all_patients = all_patients.filter(cds__district__province__code=code)
    if len(code) > 2 and len(code) <= 4:
        moh_facility = District.objects.get(code=code)
        all_patients = all_patients.filter(cds__district__code=code)
    if len(code) > 4:
        moh_facility = CDS.objects.get(code=code)
        all_patients = all_patients.filter(cds__code=code)
    sstart_date = ""
    eend_date = ""
    if "sstart_date" in request.session:
        sstart_date = request.session["sstart_date"]
        eend_date = request.session["eend_date"]
    else:
        sstart_date = request.session["sstart_date"] = ""
        eend_date = request.session["eend_date"] = ""
    if sstart_date == None or sstart_date == "":
        sstart_date = datetime.date(2012, 1, 1).strftime("%d/%m/%Y")
    if eend_date == None or eend_date == "":
        eend_date = datetime.date.today().strftime("%d/%m/%Y")
    all_patients = all_patients.filter(
        date_entry__range=[format_to_time(sstart_date), format_to_time(eend_date)]
    )

    if request.method == "POST":
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["intervention"] != "":
                all_patients = all_patients.filter(
                    Q(intervention__icontains=form.cleaned_data["intervention"])
                )
            if form.cleaned_data["sexe"] != "":
                all_patients = all_patients.filter(Q(sexe=form.cleaned_data["sexe"]))
            if form.cleaned_data["age"] != "":
                all_patients = all_patients.filter(Q(age=form.cleaned_data["age"]))
            if form.cleaned_data["colline_name"] != "":
                all_patients = all_patients.filter(
                    Q(colline_name__icontains=form.cleaned_data["colline_name"])
                )
            if form.cleaned_data["exit_status"] != "":
                all_patients = all_patients.filter(
                    Q(exit_status=form.cleaned_data["exit_status"])
                )
            if form.cleaned_data["start_date"] == None:
                form.cleaned_data["start_date"] = datetime.date(2012, 1, 1)
            if form.cleaned_data["end_date"] == None:
                form.cleaned_data["end_date"] = datetime.date.today()

            results = PatientTable(
                all_patients.filter(
                    date_entry__range=[
                        form.cleaned_data["start_date"],
                        form.cleaned_data["end_date"],
                    ]
                )
            )
            RequestConfig(request, paginate={"per_page": 1000}).configure(results)
            return render(
                request,
                "surveillance_cholera/patients.html",
                {
                    "form": form,
                    "results": results,
                    "moh_facility": moh_facility,
                    "sstart_date": request.session["sstart_date"],
                    "eend_date": request.session["eend_date"],
                },
            )

    results = PatientTable(all_patients)
    RequestConfig(request, paginate={"per_page": 1000}).configure(results)
    return render(
        request,
        "surveillance_cholera/patients.html",
        {
            "form": form,
            "results": results,
            "moh_facility": moh_facility,
            "sstart_date": request.session["sstart_date"],
            "eend_date": request.session["eend_date"],
        },
    )


########
# Alerts   ##
########
@login_required
def get_alerts(request, treshold=3):
    form = AlertForm()
    userprofile = UserProfile.objects.get(user=request.user)
    all_reports = get_all_reports(
        level=userprofile.level, moh_facility=userprofile.moh_facility
    ).filter(Q(patient__exit_status=None) | Q(patient__exit_status=""))
    the_current_date = datetime.datetime.now().date()
    if request.method == "POST":
        form = AlertForm(request.POST or None)
        if form.is_valid():
            treshold = form.cleaned_data["treshold"]
    results = all_reports.filter(
        patient__exit_status=None,
        patient__date_entry__lte=the_current_date - datetime.timedelta(days=treshold),
    ).values(
        "patient__patient_id",
        "patient__date_entry",
        "cds__name",
        "reporter__phone_number",
        "reporter__supervisor_phone_number",
    )

    return render(
        request,
        "surveillance_cholera/alerts.html",
        {"form": form, "results": results, "form": form},
    )


class ProfileUserListView(ListView):
    model = UserProfile
    paginate_by = 25


class ProfileUserDetailView(DetailView):
    model = UserProfile
    slug_field = "user"


class ProfileUserUpdateView(UpdateView):
    model = UserProfile
    fields = ("telephone",)
    exclude = ("user",)


# ProfileUser
class UserSignupView(CreateView):
    form_class = UserCreationMultiForm
    template_name = "registration/create_profile.html"

    def get_success_url(self, user):
        return reverse("profile_user_detail", kwargs={"pk": user})

    def form_valid(self, form):
        # Save the user first, because the profile needs a user before it
        # can be saved.
        user = form["user"].save()
        profile = form["profile"].save(commit=False)
        group = Group.objects.get_or_create(name=form["profile"].cleaned_data["level"])
        user.groups.add(group[0])
        profile.user = user
        profile.save()
        if (
            not form["user"].cleaned_data["password1"]
            or not form["user"].cleaned_data["password2"]
        ):
            try:
                reset_form = PasswordResetForm({"email": user.email})
                assert reset_form.is_valid()
                reset_form.save(
                    request=self.request,
                    use_https=self.request.is_secure(),
                    subject_template_name="registration/account_creation_subject.txt",
                    email_template_name="registration/account_creation_email.html",
                )
                messages.success(
                    self.request,
                    "Profile created and mail sent to {0}.".format(user.email),
                )
            except:
                messages.success(
                    self.request, "Unable to send mail  to {0}.".format(user.email)
                )
                pass
        return redirect(self.get_success_url(profile.id))


# moh_facility


def moh_facility(request):
    profile_form = UserCreationMultiForm
    cds_form = CDSForm
    district_form = DistrictForm
    province_form = ProvinceForm
    return render(
        request,
        "moh_facility.html",
        {
            "cds_form": cds_form,
            "district_form": district_form,
            "province_form": province_form,
            "profile_form": profile_form,
        },
    )
