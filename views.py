from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from HospiPal.forms import *
def index(request):

	#hashes = Hash.objects.all()
	return render(request, 'index.html')


def Patient_Management(request):

	return render(request, 'Patient_Management.html', {})

def Add_Patient(request):
	if request.method == 'POST':
		ssn = request.POST['ssn']
		try:
			person = Person.objects.get(ssn=ssn)
			return redirect('Patient_Details', pat_id = person.pk)
			pass
		except Exception, e:
			form = New_Patient_Form(initial={'ssn' : ssn})
			
			return render(request, 'new_patient_form.html', {'form' : form})
	
	form = Add_Patient_Form()
	return render(request, 'Add_Patient.html', {'form' : form})


def Search_Patient(request):
	current_url = request.get_full_path()
	form = Search_Patient_Form()

	return render(request, 'search_details.html', {'current_url' : current_url, 'form' : form })

def Patient_Details(request,pat_id=None):
	current_url = request.get_full_path()
	if request.method == 'POST':

		ssn = request.POST['ssn']
		person = Person()
		patient = Patient()
		try:
			person = Person.objects.get(ssn=ssn)
			patient = Patient.objects.get(pk=person.pk)
		except Exception, e:
			pass
		person.ssn = request.POST['ssn']
		person.date_of_birth = request.POST['date_of_birth']
		person.gender = request.POST['gender']
		person.first_name = request.POST['first_name']
		person.last_name = request.POST['last_name']
		person.street1 = request.POST['street1']
		person.street2 = request.POST['street2']
		person.city = request.POST['city']
		person.state = request.POST['state']
		person.zipcode = request.POST['zipcode']
		person.telephone = request.POST['telephone']
		patient.person = person
		patient.primary = Physician.objects.get(pk = request.POST['primary'])
		patient.illness = illness.objects.get(pk = request.POST['illness'])
		patient.hdl = request.POST['hdl']
		patient.ldl = request.POST['ldl']
		patient.tri = request.POST['tri']
		patient.blood_sugar = request.POST['blood_sugar']
		patient.needs_surgery = request.POST['needs_surgery']
		patient.date_discharged = request.POST['date_discharged']
		person.save(force_update=True)
		patient.save(force_update=True)

		return redirect('Patient_Details', pat_id = person.pk)

	form = Patient_Details_Form()
	return render(request, 'patient_details.html', {'current_url' : current_url, 'form' : form, 'pat_id' : pat_id })

def Schedule_Patient(request):
	current_url = request.get_full_path()
	form = Physician.objects.all()
	return render(request, 'patient_detail.html', {'current_url' : current_url, 'form' : form, 'key' : key })



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
