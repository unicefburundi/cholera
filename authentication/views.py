from django.views.generic import  DetailView, UpdateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from authentication.models import UserProfile
from authentication.forms import UserProfileForm
from django.core.urlresolvers import reverse
from django.shortcuts import render
from surveillance_cholera.context_processors import get_name_of_mohfacility
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from .forms import UserCreationMultiForm



class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "registration/user_detail.html"

    def get_object(self, queryset=None):
        # import ipdb; ipdb.set_trace()
        user = super(UserProfileDetailView, self).get_object(queryset)
        userprofile = UserProfile.objects.get(user=user)
        return {'user':user, 'facility':get_name_of_mohfacility(level=userprofile.level, code=userprofile.moh_facility)}



class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "registration/edit_profile.html"
    exclude = ("moh_facility", )

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})

    def post(self, request,  *args, **kwargs):
        profile = None
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)

        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, 'registration/edit_profile.html', {'form' : form})

class UserSignupView(CreateView):
    form_class = UserCreationMultiForm
    template_name = 'registration/create_profile.html'

    def get_success_url(self, user):
        return reverse( 'profile', kwargs = {'slug': user.username},)

    def form_valid(self, form):
        # Save the user first, because the profile needs a user before it
        # can be saved.
        user = form['user'].save()
        profile = form['profile'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url(user))
