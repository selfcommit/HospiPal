from django.shortcuts import render
from django.http import HttpResponse
def index(request):

	#hashes = Hash.objects.all()
	return render(request, 'index.html')


def Patient_Management(request):

	return HttpResponse("Patient_Management")

def InPatient_Management(request):

	return HttpResponse("InPatient_Management")

def MedStaff_Management(request):

	return HttpResponse("MedStaff_Management")
# Create your views here.
