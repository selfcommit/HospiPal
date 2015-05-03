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


class NewPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['hdl', 'ldl',
                  'tri', 'primary', 'blood_sugar',
                  'needs_surgery']
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class ExistingPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['person', 'hdl', 'ldl',
                  'tri', 'primary', 'blood_sugar',
                  'needs_surgery']
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class AssignBedForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                     required=True
                                     )
    bed = forms.ModelChoiceField(queryset=Bed.objects.filter(available=True))


class AssignDoctorForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                     required=True
                                     )
    doctor = forms.ModelChoiceField(queryset=Physician.objects.all())


class AssignNurseForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                     required=True
                                     )
    nurse = forms.ModelChoiceField(queryset=Nurse.objects.all())


class NewSurgeonForm(ModelForm):
    class Meta:
        model = Surgeon
        fields = ['skills', 'salary_amount']


class SurgeryFormStep1(forms.Form):
    surgery_type = forms.ModelChoiceField(queryset=Surgery_Type.objects.all())


class NewSurgeryForm(ModelForm):
    surgery_type = forms.ModelChoiceField(queryset=Surgery_Type.objects.all(),
                                          required=False,
                                          widget=forms.HiddenInput())

    class Meta:
        model = Surgery
        fields = ['surgery_type', 'date_performed', 'nurses',
                  'surgeons', 'patient', 'theater']
        widgets = {'date_performed': SelectDateWidget(
                                     years=range(
                                         date.today().year,
                                         date.today().year + 2))}


class NewSurgeryTypeForm(ModelForm):

    class Meta:
        model = Surgery_Type
        fields = ['name', 'category', 'anatomical_location', 'special_needs',
                  'skills']


class NewPhysicianForm(ModelForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    required=False, widget=forms.HiddenInput())

    class Meta:
        model = Physician
        fields = ['skill', 'person', 'ownership', 'salary_amount']


class NewSkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class NewNurseForm(ModelForm):
    class Meta:
        model = Nurse
        fields = ['years_experience', 'skill', 'grade', 'salary_amount']


class NewTheaterForm(ModelForm):
    class Meta:
        model = Theater
        fields = ['name']


class NewSupportStaffForm(ModelForm):
    class Meta:
        model = SupportStaff
        fields = ['salary_amount']
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


class ViewDoctorSchedule(forms.Form):
    physician = forms.ModelChoiceField(queryset=Physician.objects.all(),
                                       required=True)


class ViewDailySchedule(forms.Form):
    date = forms.DateField(widget=SelectDateWidget(
                           years=range(date.today().year,
                                       date.today().year + 2)))
    physician = forms.ModelChoiceField(queryset=Physician.objects.all(),
                                       required=True)


class SearchPatientForm(forms.Form):
    ssn = forms.IntegerField()
    first_name = forms.CharField(max_length=33)
    last_name = forms.CharField(max_length=33)


class SearchStaffForm(forms.Form):
    ssn = forms.IntegerField()
    first_name = forms.CharField(max_length=33)
    last_name = forms.CharField(max_length=33)


class SchedulePatientForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    physician = forms.ModelChoiceField(queryset=Physician.objects.all(), required=True)
    date_of_consult = forms.DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year + 2)))
    time_of_consult = forms.TimeField(initial=datetime.now().strftime('%H:%M'), input_formats=['%H:%M'])
