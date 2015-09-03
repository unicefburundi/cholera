from surveillance_cholera.forms import SearchForm
from authentication.models import UserProfile
from surveillance_cholera.models import CDS, District, Province

def get_name_of_mohfacility(level='',code=''):
    if level=='CDS':
        return CDS.objects.get(code=code)
    if level=='BDS':
        return District.objects.get(code=code)
    if level=='BPS':
        return Province.objects.get(code=code)
    if level=='CEN':
        return 'Central'

def search_form(request):
    if request.user.is_authenticated:
        return { 'search_form' : SearchForm(request) }

def myfacility(request):
    myprofile = None
    try:
        myprofile = UserProfile.objects.get(user=request.user)
    except TypeError:
        return {}
    # import ipdb; ipdb.set_trace()

    return {'myprofile':myprofile, 'mycode':myprofile.moh_facility , 'mylevel': myprofile.level, 'myfacility' : get_name_of_mohfacility(level=myprofile.level, code=myprofile.moh_facility)  }