from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from HospiPal.forms import *
from django.db.models import Q
import datetime


def index(request):

    # hashes = Hash.objects.all()
    return render(request, 'index.html')


def Search(request):

    return render(request, 'search.html', {})


def NewPatient(request):
    title = 'New Patient Form'
    form1 = NewPersonForm()
    form2 = NewPatientForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewPatientForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            form2.person = person
            p = form2.save()
            return redirect('Patient_Management')
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Patient_Management(request):

    return render(request, 'Patient_Management.html', {})


def Add_Patient(request):
    current_url = request.get_full_path()
    form = NewPatientForm()
    if request.method == 'POST':
        form = NewPatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            # for pk in illness_pks:
            #    illness_type = Illness_Type.objects.get(pk=pk)
            #    illness = Illness()
            #    illness.name = illness_type
            #    illness.save()
            #    illness_list.append(illness)
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'add.html',
                  {'patient_form': form, 'current_url': current_url})


def Patient_Details(request, pat_id=None):
    current_url = request.get_full_path()
    patient = get_object_or_404(Patient, pk=pat_id)
    appointments = Consultation.objects.filter(patient=patient)
    illness_history = Illness.objects.filter(patient=patient)
    p = model_to_dict(patient)
    return render(request, 'patient_details.html',
                           {'current_url': current_url,
                            'appointments': appointments,
                            'patient': patient,
                            'illness_history': illness_history, 'p': p})


def Search_Patient(request):
    if request.method == 'POST':
        ssn = request.POST.get('ssn', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)

        patients = Patient.objects.filter(Q(person__ssn__startswith=ssn) |
                                          Q(person__first_name__startswith=first_name) |
                                          Q(person__last_name__startswith=last_name))

        return render(request, 'search_details.html', {'patients': patients})

    current_url = request.get_full_path()
    form = Search_Patient_Form()

    return render(request, 'search.html', {'current_url': current_url, 'form': form})


def Schedule_Patient(request):
    form = SchedulePatientForm()
    if request.method == 'POST':
        form = SchedulePatientForm(request.POST)
        if form.is_valid:
            time = request.POST['time_of_consult'].split(':')
            c = Consultation()
            c.patient = Patient.objects.get(pk=request.POST['patient'])
            c.doctor = Physician.objects.get(pk=request.POST['physician'])
            c.date_of_consult = datetime.datetime(
                        day=int(request.POST['date_of_consult_day']),
                        month=int(request.POST['date_of_consult_month']),
                        year=int(request.POST['date_of_consult_year']),
                        hour=int(time[0]),
                        minute=int(time[1]))
            c.save()

            return redirect('Patient_Details', pat_id=c.patient.pk)

    return render(request, 'schedule_patient.html', {'form': form})


def Doctor_Schedule(request):
    form = ViewDoctorSchedule()
    current_url = request.get_full_path()
    title = "View Schedule by Doctor"
    appointments = []
    if request.method == 'POST':
        doctor = Physician.objects.get(pk=request.POST.get('physician', None))
        appointments = Consultation.objects.filter(doctor=doctor).filter(
                       date_of_consult__gte=datetime.date.today())

    return render(request, 'schedule.html', {'form': form,
                                             'current_url': current_url,
                                             'title': title,
                                             'appointments': appointments})


def Daily_Schedule(request):
    form = ViewDailySchedule()
    current_url = request.get_full_path()
    title = "View Schedule by Date"
    appointments = []
    date = []
    if request.method == 'POST':
        day = int(request.POST['date_day'])
        month = int(request.POST['date_month'])
        year = int(request.POST['date_year'])

        date = datetime.datetime(day=day,
                                 month=month,
                                 year=year,
                                 hour=0,
                                 minute=0,
                                 ).strftime('%Y-%m-%d %H:%M')
        doctor = Physician.objects.get(pk=request.POST.get('physician', None))
        appointments = Consultation.objects.filter(
                       date_of_consult__gte=date).filter(doctor=doctor)

    return render(request, 'schedule.html', {'form': form,
                                             'current_url': current_url,
                                             'title': title,
                                             'appointments': appointments})


def InPatient_Management(request):
    bed_count = Bed.objects.filter(available=True).count()

    return render(request, 'InPatient_Management.html', {'bed_count':
                                                         bed_count})


def Assign_Bed(request):
    form = AssignBedForm()
    current_url = request.get_full_path()
    title = 'Assign a Bed'

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title})


def Assign_Doctor(request):
    form = AssignDoctorForm()
    current_url = request.get_full_path()
    title = 'Assign a Doctor'

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title})


def Assign_Nurse(request):
    form = AssignNurseForm()
    current_url = request.get_full_path()
    title = 'Assign a Nurse'

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title})


def Remove_Bed(request):

    return HttpResponse("InPatient_Management")


def Book_Surgery(request):
    form = NewSurgeryForm()
    nurses = Nurse.objects.all()
    surgeons = Surgeon.objects.all()

    return render(request, 'schedule.html', {'nurses': nurses,
                                             'surgeons': surgeons})


def View_Surgery(request):

    return HttpResponse("InPatient_Management")


def MedStaff_Management(request):

    return render(request, 'MedStaff_Management.html')


def Schedule_MedStaff(request):
    pass


def Search_MedStaff(request):
    return HttpResponse('Oh look Medstaff!')
    pass


def Remove_MedStaff(request):
    if request.method == 'POST':
        return HttpResponse('Tried to remove someone')

    nurses = Nurse.objects.all()
    physicians = Physician.objects.all()
    surgeons = Surgeon.objects.all()
    gen_staff = SupportStaff.objects.all()
    return render(request, 'remove_staff.html', {'nurses': nurses,
                                                 'physicians': physicians,
                                                 'surgeons': surgeons,
                                                 'gen_staff': gen_staff})


def Add_MedStaff(request):
    pass


def Add_Physician(request, person_id=None, staff_id=None):
    title = 'New Physician Form'
    form1 = NewPersonForm()
    form2 = NewPhysicianForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewPhysicianForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            form2.person = person
            p = form2.save()
            return redirect('Search_MedStaff')
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Add_Nurse(request):
    title = 'New Nurse Form'
    form1 = NewPersonForm()
    form2 = NewNurseForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewNurseForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            form2.person = person
            p = form2.save()
            return redirect('Search_MedStaff')
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Add_Surgeon(request):
    form1 = NewPersonForm()
    form2 = NewSurgeonForm()
    title = 'New Surgeon Form'
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewSurgeonForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            form2.person = person
            p = form2.save()
            return redirect('Search_MedStaff')
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Add_Support(request):
    form1 = NewPersonForm()
    form2 = NewSupportStaffForm()
    title = 'New Support Staff Form'
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewSupportStaffForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            form2.person = person
            p = form2.save()
            return redirect('Search_MedStaff')
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Add_Chief(request):
    if request.method == 'POST':
        return HttpResponse('Things and stuff')
    else:
        return Http404()


def AddSkill(request):
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewSkillForm()
    return render(request, 'add.html', {'form': form, 'current_url': current_url})


def Schedule_MedStaff(request):
    pass
