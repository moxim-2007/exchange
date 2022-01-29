from django import forms

from .models import Company


class LoginForm(forms.Form):
    username = forms.CharField(label="Username:")
    password = forms.CharField(label="Password ", widget=forms.PasswordInput)


class RegForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = (
            "username",
            "email",
            "name",
            "description",
            "legal_address",
            "image",
        )

    def check_passwords(self):
        cd = self.cleaned_data
        if cd["password"] == cd["password2"]:
            raise forms.ValidationError("Password mismatch")
        return cd["password"]


class UserEditForm(forms.ModelForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="New password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = Company
        fields = (
            "username",
            "email",
            "name",
            "description",
            "legal_address",
            "image",
        )

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if old_password == new_password:
            raise Exception("Old password and new password match")
        return self.cleaned_data
