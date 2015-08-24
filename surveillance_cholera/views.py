from surveillance_cholera.models import Person
from django.views.generic import ListView

class PersonListView(ListView):
    model = Person
    paginate_by = 10  #and that's it !!