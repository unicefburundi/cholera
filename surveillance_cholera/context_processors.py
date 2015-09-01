from surveillance_cholera.forms import SearchForm

def search_form(request):
    if request.user.is_authenticated:
        return { 'search_form' : SearchForm(request) }
    else:
        return { 'search_form' : SearchForm() }