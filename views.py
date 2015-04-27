from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from HospiPal.forms import *
from django.db.models import Q


def index(request):

    # hashes = Hash.objects.all()
    return render(request, 'index.html')


def AddPerson(request):
    person_form = NewPersonForm()
    if request.method == 'POST':
        person_form = NewPersonForm(request.POST)
        if person_form.is_valid():
            # person_form.save(commit=False) # generate model without closing
            person_form.save()
            return redirect('index')

    return render(request, 'add_person.html',
                  {'person_form': person_form})


def Patient_Management(request):

    return render(request, 'Patient_Management.html', {})


def Add_Patient(request):
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

    return render(request, 'add_patient.html',
                  {'patient_form': form})


def Patient_Details(request, pat_id=None):
    current_url = request.get_full_path()
    patient = get_object_or_404(Patient, pk=pat_id)
    appointments = Consultation.objects.filter(patient=patient)
    p = model_to_dict(patient)
    return render(request, 'patient_details.html',
                           {'current_url': current_url,
                            'appointments': appointments,
                            'patient': patient, 'p': p})


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
            c.date_of_consult = datetime(
                        day=int(request.POST['date_of_consult_day']),
                        month=int(request.POST['date_of_consult_month']),
                        year=int(request.POST['date_of_consult_year']),
                        hour=int(time[0]),
                        minute=int(time[1]))
            c.save()

            return redirect('Patient_Details', pat_id=c.patient.pk)

    return render(request, 'schedule_patient.html', {'form': form})


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

    return render(request, 'medstaff_management.html')


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
    gen_staff = Staff.objects.filter(staff_type__contains='T')

    return render(request, 'remove_staff.html', {'nurses': nurses,
                                                 'physicians': physicians,
                                                 'surgeons': surgeons,
                                                 'gen_staff': gen_staff})


def Add_MedStaff(request):
    form = NewStaffForm()
    if request.method == 'POST':
        form = NewStaffForm(request.POST)
        if form.is_valid():
            staff = form.save()
            if staff.staff_type == 'P':
                form = NewPhysicianForm()
                form.person = staff.person.pk
                form.staff = staff.pk
                return render(request, 'add_physician.html', {'form': form})
            if staff.staff_type == 'N':
                return HttpResponse('Add Nurse')
            if staff.staff_type == 'S':
                return HttpResponse('Add Surgeon')
            if staff.staff_type == 'T':
                return HttpResponse('Add support Staff')
            if staff.staff_type == 'C':
                return HttpResponse('Add Chief')

    return render(request, 'new_staff.html', {'form': form})


def Add_Physician(request, person_id=None, staff_id=None):
    if request.method == 'POST':
        person = Person.objects.get(pk=person_id)
        staff = Staff.objects.get(pk=staff_id)
        p = Physician()
        p.person = person
        p.staff = staff
        p.ownership = request.POST.get('ownership', False)
        p.skill = Skill.objects.get(pk=request.POST['skill'])
        p.save()
        return HttpResponse(p)

        return redirect('Search_MedStaff')
    else:
        return Http404()


def Add_Nurse(request):
    if request.method == 'POST':
        return HttpResponse('Things and stuff')
    else:
        return Http404()


def Add_Surgeon(request):
    if request.method == 'POST':
        return HttpResponse('Things and stuff')
    else:
        return Http404()


def Add_Support(request):
    if request.method == 'POST':
        return HttpResponse('Things and stuff')
    else:
        return Http404()


def Add_Chief(request):
    if request.method == 'POST':
        return HttpResponse('Things and stuff')
    else:
        return Http404()


def AddSkill(request):
    form = NewSkillForm()
    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('New Skill Saved.')

    return render(request, 'add_skill.html', {'form': form})


def Schedule_MedStaff(request):
    pass
