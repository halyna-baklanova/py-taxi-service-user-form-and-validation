from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_part = license_number[:3]
        second_part = license_number[3:]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure the number consist of 8 characters"
            )
        if not first_part.isalpha() or not first_part.isupper():
            raise ValidationError(
                "First 3 characters should be the upper case letter"
            )
        if not second_part.isdigit():
            raise ValidationError(
                "Last 5 characters should be "
            )

        return license_number


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
