from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
	# Examples:
urlpatterns = patterns('',

	#Example /1/ (Show Details)
	url(r'^PM/$', 'HospiPal.views.Patient_Management', name = 'Patient_Management'),
	url(r'^IPM/$', 'HospiPal.views.InPatient_Management', name = 'InPatient_Management'),
	url(r'^MSM/$', 'HospiPal.views.MedStaff_Management', name = 'MedStaff_Management'),
	
)