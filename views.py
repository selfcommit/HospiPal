from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from HospiPal.forms import *
def index(request):

	#hashes = Hash.objects.all()
	return render(request, 'index.html')


def Patient_Management(request):

	return render(request, 'Patient_Management.html', {})

def Add_Patient(request):
	if request.method == 'POST':
		form = New_Patient_Form(request.POST)
		if form.is_valid():
			ssn = request.POST['ssn']
			primary_pk = request.POST['Primary']
			nurse_pk = request.POST['Nurse']
			illness_pks = request.POST['illness']
			illness_list = []

			for pk in illness_pks:
				illness_type = Illness_Type.objects.get(pk = pk)
				illness = Illness()
				illness.name = illness_type
				illness.save()
				illness_list.append(illness)
			primary = Physician.objects.get(pk=primary_pk )
			nurse = Nurse.objects.get(pk=nurse_pk)
			try:
				person = Person.objects.get(ssn=ssn)
				patient.person = person
				patient.primary = primary
				patient.illness = illness_list
				patient.hdl = request.POST['hdl']
				patient.ldl = request.POST['ldl']
				patient.tri = request.POST['tri']
				patient.blood_sugar = request.POST['blood_sugar']
				patient.needs_surgery = request.POST.get('needs_surgery', False)
				patient.attending_nurse = nurse
				patient.save()
				return redirect('Patient_Details', pat_id = person.pk)
			except Exception, e:
				person = Person()
				patient = Patient()

			person.ssn = request.POST['ssn']
			birth_day = request.POST['date_of_birth_day']
			birth_month = request.POST['date_of_birth_month']
			birth_year = request.POST['date_of_birth_year']
			person.date_of_birth = birth_year+'-'+birth_month+'-'+birth_day
			person.gender = request.POST['gender']
			person.first_name = request.POST['first_name']
			person.last_name = request.POST['last_name']
			person.street1 = request.POST['street1']
			person.street2 = request.POST['street2']
			person.city = request.POST['city']
			person.state = request.POST['state']
			person.zipcode = request.POST['zipcode']
			person.telephone = request.POST['telephone']
			person.save()
			patient.person = person
			patient.primary = primary
			patient.illness = illness_list
			patient.hdl = request.POST['hdl']
			patient.ldl = request.POST['ldl']
			patient.tri = request.POST['tri']
			patient.blood_sugar = request.POST['blood_sugar']
			patient.needs_surgery = request.POST.get('needs_surgery', False)
			patient.attending_nurse = nurse
			patient.save()

			return redirect('Patient_Details', pat_id = person.pk)
		else:
			return render(request, 'new_patient_form.html', {'form' : form})				
	
	form = New_Patient_Form()
	return render(request, 'new_patient_form.html', {'form' : form})

def Patient_Details(request,pat_id=None):
	current_url = request.get_full_path()
	patient = get_object_or_404(Patient, pk=pat_id)
	p = model_to_dict(patient)
	return render(request, 'patient_details.html', {'current_url' : current_url, 'patient' : patient, 'p' : p })

def Search_Patient(request):
	current_url = request.get_full_path()
	form = Search_Patient_Form()

	return render(request, 'search_details.html', {'current_url' : current_url, 'form' : form })


def Schedule_Patient(request):
	current_url = request.get_full_path()
	return HttpResponse('Schedule_Doctor')



def InPatient_Management(request):

	return HttpResponse("InPatient_Management")

def Assign_Bed(request):

	return HttpResponse("InPatient_Management")

def Remove_Bed(request):

	return HttpResponse("InPatient_Management")

def Book_Surgery(request):

	return HttpResponse("InPatient_Management")

def View_Surgery(request):

	return HttpResponse("InPatient_Management")

def MedStaff_Management(request):

	return HttpResponse("MedStaff_Management")

def Schedule_MedStaff(request):
	pass

def Search_MedStaff(request):
	pass

def Remove_MedStaff(request):
	pass

def Add_MedStaff(request):
	pass

def Schedule_MedStaff(request):
	pass
