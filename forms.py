from datetime import *
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets
from HospiPal.models import *

# class Add_Patient_Form(forms.Form):
#   def __init__(self, *args, **kwargs):
#       super(Add_Patient_Form, self).__init__(*args, **kwargs)

#   ssn = forms.IntegerField(label="Enter SSN")
    # self.fields['illness'] = forms.ChoiceField(choices=illness_choices)


class NewPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['ssn', 'gender', 'first_name', 'last_name',
                  'date_of_birth', 'street1', 'street2',
                  'city', 'state', 'zipcode', 'telephone']
        widgets = {'date_of_birth': SelectDateWidget(years=range(1920, 2025))}


class NewStaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['person', 'salary_amount', 'staff_type']


class NewPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['person', 'primary', 'attending_nurse',
                  'hdl', 'ldl', 'tri', 'blood_sugar',
                  'needs_surgery']
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class NewSurgeonForm(ModelForm):
    class Meta:
        model = Surgeon
        fields = ['skills']


class NewPhysicianForm(ModelForm):
    class Meta:
        model = Physician
        fields = ['skill', 'ownership']


class NewSkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class NewNurseForm(ModelForm):
    class Meta:
        model = Nurse
        fields = ['years_experience', 'skill', 'grade']

    # ssn = forms.IntegerField()
    # date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1920, 2025)))
    # gender = forms.ChoiceField(choices=GENDER_CHOICE)
    # first_name = forms.CharField(max_length=33)
    # last_name = forms.CharField(max_length=33)
    # street1 = forms.CharField(max_length=255)
    # street2 = forms.CharField(max_length=255, required=False)
    # city = forms.CharField(max_length=255)
    # state = forms.CharField(max_length=255)
    # zipcode = forms.CharField(max_length=255)
    # telephone = forms.CharField(max_length=33)
    # Primary = forms.ModelChoiceField(queryset=Physician.objects.all())
    # Nurse = forms.ModelChoiceField(queryset=Nurse.objects.all())
    # hdl = forms.CharField(max_length=33)
    # ldl = forms.CharField(max_length=33)
    # tri = forms.CharField(max_length=33)
    # blood_sugar = forms.CharField(max_length=33)
    # needs_surgery = forms.BooleanField(required=False)


class Prescription(forms.Form):
    # illness = forms.ModelMultipleChoiceField(queryset=Illness_Type.objects.all())
    pass


class Search_Patient_Form(forms.Form):
    ssn = forms.IntegerField()
    first_name = forms.CharField(max_length=33)
    last_name = forms.CharField(max_length=33)


class SchedulePatientForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    physician = forms.ModelChoiceField(queryset=Physician.objects.all(), required=True)
    date_of_consult = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year + 2)))
    time_of_consult = forms.TimeField(initial=datetime.now().strftime('%H:%M'), input_formats=['%H:%M'])
