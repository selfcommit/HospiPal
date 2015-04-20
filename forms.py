from django import forms
from HospiPal.models import *

class Add_Patient_Form(forms.Form):
	def __init__(self, *args, **kwargs):
		super(Add_Patient_Form, self).__init__(*args, **kwargs)
		
	ssn = forms.IntegerField(label="Enter SSN")	
	#self.fields['illness'] = forms.ChoiceField(choices=illness_choices)
	
	
class New_Patient_Form(forms.Form):
	
	GENDER_CHOICE = (
	('M', 'Male'),
	('F', 'Female'),
	)
	ssn = forms.IntegerField()
	date_of_birth = forms.DateField()
	gender = forms.ChoiceField(choices=GENDER_CHOICE)
	first_name = forms.CharField(max_length = 33)
	last_name =  forms.CharField(max_length = 33)
	street1 = forms.CharField(max_length=255)
	street2 = forms.CharField(max_length=255)
	city = forms.CharField(max_length=255)
	state = forms.CharField(max_length=255)
	zipcode = forms.CharField(max_length=255)
	telephone = forms.CharField(max_length=33)
	Primary = forms.ModelChoiceField(queryset=Physician.objects.all())
	#illness = forms.ModelChoiceField(queryset=Illness_Type.objects.all())
	illness = forms.ModelMultipleChoiceField(queryset=Illness_Type.objects.all())
	Nurse = forms.ModelChoiceField(queryset=Nurse.objects.all())
	hdl = forms.CharField(max_length = 33)
	ldl = forms.CharField(max_length = 33)
	tri = forms.CharField(max_length = 33)
	blood_sugar = forms.CharField(max_length = 33)
	needs_surgery = forms.BooleanField()

class Patient_Details_Form(forms.Form):
	
	GENDER_CHOICE = (
	('M', 'Male'),
	('F', 'Female'),
	)
	ssn = forms.IntegerField()
	date_of_birth = forms.DateField()
	gender = forms.ChoiceField(choices=GENDER_CHOICE)
	first_name = forms.CharField(max_length = 33)
	last_name =  forms.CharField(max_length = 33)
	street1 = forms.CharField(max_length=255)
	street2 = forms.CharField(max_length=255)
	city = forms.CharField(max_length=255)
	state = forms.CharField(max_length=255)
	zipcode = forms.CharField(max_length=255)
	telephone = forms.CharField(max_length=33)
	Primary = forms.ModelChoiceField(queryset=Physician.objects.all())
	#illness = forms.ModelChoiceField(queryset=Illness_Type.objects.all())
	illness = forms.ModelMultipleChoiceField(queryset=Illness_Type.objects.all())
	Nurse = forms.ModelChoiceField(queryset=Nurse.objects.all())
	hdl = forms.CharField(max_length = 33)
	ldl = forms.CharField(max_length = 33)
	tri = forms.CharField(max_length = 33)
	blood_sugar = forms.CharField(max_length = 33)
	needs_surgery = forms.BooleanField()

class Search_Patient_Form(forms.Form):
	ssn = forms.IntegerField()
	first_name = forms.CharField(max_length = 33)
	last_name = forms.CharField(max_length = 33)
