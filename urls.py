from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
	# Examples:
urlpatterns = patterns('',

	#Example /1/ (Show Details)
	url(r'^PM/$', 'HospiPal.views.Patient_Management', name = 'Patient_Management'),
	url(r'^PM/add/$', 'HospiPal.views.Add_Patient', name = 'Add_Patient'),
	url(r'^PM/details/$','HospiPal.views.Patient_Details', name = 'Patient_Details'),
	url(r'^PM/details/(?P<pat_id>\d+)/$','HospiPal.views.Patient_Details', name = 'Patient_Details'),
	url(r'^PM/search/$', 'HospiPal.views.Search_Patient', name = 'Search_Patient'),
	url(r'^PM/sched/$', 'HospiPal.views.Schedule_Patient', name = 'Schedule_Patient'),
	url(r'^IPM/$', 'HospiPal.views.InPatient_Management', name = 'InPatient_Management'),
	url(r'^IPM/assign/$', 'HospiPal.views.Assign_Bed', name = 'Assign_Patient'),
	url(r'^IPM/remove/$', 'HospiPal.views.Remove_Bed', name = 'Remove_Patient'),
	url(r'^IPM/book/$', 'HospiPal.views.Book_Surgery', name = 'Book_Surgery'),
	url(r'^IPM/view/$', 'HospiPal.views.View_Surgery', name = 'View_Surgery'),
	url(r'^MSM/$', 'HospiPal.views.MedStaff_Management', name = 'MedStaff_Management'),
	url(r'^MSM/add/$', 'HospiPal.views.Add_MedStaff', name = 'Add_Medstaff'),
	url(r'^MSM/remove/$', 'HospiPal.views.Remove_MedStaff', name = 'Remove_MedStaff'),
	url(r'^MSM/search/$', 'HospiPal.views.Search_MedStaff', name = 'Search_MedStaff'),
	url(r'^MSM/sched/$', 'HospiPal.views.Schedule_MedStaff', name = 'Schedule_MedStaff')
	
)