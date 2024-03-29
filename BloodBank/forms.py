from django import forms
from django.forms import ModelForm
from .models import Donor, Teams, Events, Requests, ContactUs
from .choices import*
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column



class DonorForm(ModelForm):
    class Meta:
        model = Donor
        fields = ['name','age','phone','address','gender','bloodgroup','unit']

    BLOODGROUP_CHOICES = (
    (("A+", "A+")),
    (("A-", "A-")),
    (("B+", "B+")),
    (("B-", "B-")),
    (("O+", "O+")),
    (("O-", "O-")),
    (("AB+", "AB+")),
    (("AB-", "AB-")),
)

class AskBloodForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields =  ['name','phone','email','bloodgroup','unit','note']
       

      

    def __init__(self, *args,**kwargs):
        super().__init__ (*args, **kwargs)
        self.helper=FormHelper()
        self.helper.layout= Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('bloodgroup', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('unit', css_class='form-group col-md-6 mb-0'),
                Column('note', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )
        self.helper.add_input(Submit('Submit_form','Submit', css_class='btn btn-danger controls offset-md-3 col-md-6'))

        

class EventForm(ModelForm):
    class Meta:
        model=Events
        fields="__all__"

    
class TeamForm(ModelForm):
    class Meta:
        model=Teams
        fields="__all__"

class ContactUsForm(ModelForm):
    class Meta:
        model=ContactUs
        fields="__all__"
       