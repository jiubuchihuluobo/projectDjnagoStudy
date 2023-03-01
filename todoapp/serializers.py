from django.forms.models import ModelForm

from customauth.models import User
from todoapp.models import Profile


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(ModelForm):
    def save(self, commit=True):
        super(ProfileUpdateForm, self).save()

    class Meta:
        model = Profile
        fields = ["avatar"]
