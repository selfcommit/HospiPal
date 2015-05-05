from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from HospiPal.forms import *
from django.db.models import Q
from django.db.models import get_model
from itertools import chain
import datetime


def index(request):

    return render(request, 'index.html')


def Search(request):
    current_url = request.get_full_path()
    search_text = request.GET.get('searchbox', None)
    title = 'Search Results for: '
    patients = Patient.objects.filter(Q(person__ssn__startswith=search_text) |
                                      Q(person__first_name__startswith=search_text) |
                                      Q(person__last_name__startswith=search_text))
    doctor_list = Physician.objects.filter(Q(person__ssn__startswith=search_text) |
                                           Q(person__first_name__startswith=search_text) |
                                           Q(person__last_name__startswith=search_text))
    nurse_list = Nurse.objects.filter(Q(person__ssn__startswith=search_text) |
                                      Q(person__first_name__startswith=search_text) |
                                      Q(person__last_name__startswith=search_text))
    surgeon_list = Surgeon.objects.filter(Q(person__ssn__startswith=search_text) |
                                          Q(person__first_name__startswith=search_text) |
                                          Q(person__last_name__startswith=search_text))
    support_list = SupportStaff.objects.filter(Q(person__ssn__startswith=search_text) |
                                               Q(person__first_name__startswith=search_text) |
                                               Q(person__last_name__startswith=search_text))

    staff = list(chain(doctor_list, nurse_list, surgeon_list, support_list))

    surgerys = Surgery.objects.filter(Q(surgery_type__name__startswith=search_text) |
                                      Q(theater__name__startswith=search_text))

    return render(request, 'search_details.html', {'current_url': current_url,
                                                   'search_text': search_text,
                                                   'patients': patients,
                                                   'title': title,
                                                   'staff': staff,
                                                   'surgerys': surgerys})


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
            patient = form2.save(commit=False)
            patient.person = person
            form2.save()
            return redirect('Patient_Details', pat_id=patient.pk)
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
    form = ExistingPatientForm()
    title = "Add Existing Patient"
    if request.method == 'POST':
        form = ExistingPatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'add.html',
                  {'form': form, 'current_url': current_url,
                   'title': title})


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
    form = SearchPatientForm()

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
    initial = {'patient': request.GET.get('patient', None)}
    form = AssignBedForm(initial=initial)
    current_url = request.get_full_path()
    title = 'Assign a Bed'
    if request.method == 'POST':
        form = AssignBedForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=request.POST.get('patient', None))
            bed = Bed.objects.get(pk=request.POST.get('bed', None))
            patient.bed = bed
            bed.available = False
            bed.save()
            patient.save()
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title,
                                           'initial': initial})


def Add_Illness(request):
    initial = {'patient': request.GET.get('patient', None)}
    form = NewIllnessForm(initial=initial)
    current_url = request.get_full_path()
    title = 'Assign an Illness'
    if request.method == 'POST':
        form = NewIllnessForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=request.POST.get('patient', None))
            form.save()
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title,
                                           'initial': initial})


def Add_Prescript(request):
    initial = {'patient': request.GET.get('patient', None)}
    current_url = request.get_full_path()
    title = "Add prescription to Patient"
    form = NewPrescriptForm(initial=initial)

    if request.method == 'POST':
        form = NewPrescriptForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('Patient_Details',
                            pat_id=request.POST.get('patient', None))

    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'title': title})


def Assign_Discharge(request):
    initial = {'patient': request.GET.get('patient', None)}
    form = AssignDischargeForm(initial=initial)
    current_url = request.get_full_path()
    title = "Assign discharge Date"

    if request.method == 'POST':
        form = AssignDischargeForm(request.POST, initial=initial)
        if form.is_valid():
            patient = Patient.objects.get(pk=request.POST.get('patient', None))
            time = request.POST['time'].split(':')
            day = int(request.POST['date_day'])
            month = int(request.POST['date_month'])
            year = int(request.POST['date_year'])
            hour = int(time[0])
            minute = int(time[1])

            date = datetime.datetime(day=day,
                                     month=month,
                                     year=year,
                                     hour=hour,
                                     minute=minute,
                                     ).strftime('%Y-%m-%d %H:%M')

            patient.date_discharged = date
            patient.save()
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title,
                                           'initial': initial})


def Assign_Doctor(request):
    title = 'Assign a Doctor'
    form = AssignDoctorForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = AssignDoctorForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=request.POST.get('patient', None))
            doctor = Physician.objects.get(pk=request.POST.get('doctor', None))
            patient.physician = doctor
            patient.save()
            return redirect('Patient_Details', pat_id=patient.pk)

    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title})


def Assign_Nurse(request):
    title = 'Assign a Nurse'
    form = AssignNurseForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = AssignNurseForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=request.POST.get('patient', None))
            nurse = Nurse.objects.get(pk=request.POST.get('nurse', None))
            patient.attending_nurse = nurse
            patient.save()
            return redirect('Patient_Details', pat_id=patient.pk)
    return render(request, 'assign.html', {'form': form,
                                           'current_url': current_url,
                                           'title': title})


def Remove_Bed(request):

    return HttpResponse("InPatient_Management")


def Book_Surgery(request):
    form = SurgeryFormStep1()
    current_url = request.get_full_path()
    title = 'Step1: Select Surgery Type'
    step = 'step1'
    if request.method == 'POST':
        if 'step1' in request.POST:
            form = SurgeryFormStep1(request.POST)
            if form.is_valid():
                step = 'step2'
                title = 'Step2: Select Staff and Date'
                surgery_type = request.POST.get('surgery_type', None)
                surgery_type = Surgery_Type.objects.get(pk=surgery_type)
                skills = surgery_type.skills.all
                nurses = Nurse.objects.filter(skill=skills)
                surgeons = Surgeon.objects.filter(skills=skills)
                initial = {'patient': request.GET.get('patient', None)}
                form = NewSurgeryForm(request.POST, initial=initial)

                return render(request, 'schedule.html',
                              {'form': form,
                               'current_url': current_url,
                               'skills': skills,
                               'surgery_type': surgery_type,
                               'step': step,
                               'title': title
                               })
        if 'step2' in request.POST:
            form = NewSurgeryForm(request.POST)

            if form.is_valid():
                surgery_type = request.POST.get('surgery_type', None)
                surgery_type = Surgery_Type.objects.get(pk=surgery_type)
                s = form.save(commit=False)
                s.surgery_type = surgery_type
                s.date_performed = datetime.datetime(
                    day=int(request.POST['date_performed_day']),
                    month=int(request.POST['date_performed_month']),
                    year=int(request.POST['date_performed_year']),
                    )
                s.save()
                form.save_m2m()
                # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
                return redirect('Surgery_Details', sid=s.pk)

    return render(request, 'schedule.html', {'form': form,
                                             'current_url': current_url,
                                             'title': title,
                                             'step': step})


def View_Surgery(request):
    current_url = request.get_full_path()

    item_list = Surgery.objects.all()

    return render(request, 'list.html', {'item_list': item_list,
                                         'current_url': current_url})


def Surgery_Details(request, sid=None):
    current_url = request.get_full_path()  
    surgery = get_object_or_404(Surgery, pk=sid)

    return render(request, 'surgery.html', {'surgery': surgery,
                                            'current_url': current_url})


def MedStaff_Management(request):

    return render(request, 'MedStaff_Management.html')


def Schedule_MedStaff(request):
    pass


def Search_MedStaff(request):
    doctor_list = Physician.objects.all()
    nurse_list = Nurse.objects.all()
    surgeon_list = Surgeon.objects.all()
    support_list = SupportStaff.objects.all()

    current_url = request.get_full_path()

    return render(request, 'staff_list.html', {'doctor_list': doctor_list,
                                               'nurse_list': nurse_list,
                                               'surgeon_list': surgeon_list,
                                               'support_list': support_list,
                                               'current_url': current_url,
                                               })


def Staff_Details(request, staff_id=None):
    current_url = request.get_full_path()
    staff_list = []
    person = get_object_or_404(Person, pk=staff_id)
    physician = Physician.objects.filter(person=person)
    nurse = Nurse.objects.filter(person=person)
    surgeon = Surgeon.objects.filter(person=person)
    staff = SupportStaff.objects.filter(person=person)

    if physician:
        staff_list.append(physician)
    if nurse:
        staff_list.append(nurse)
    if surgeon:
        staff_list.append(surgeon)
    if staff:
        staff_list.append(staff)
    return render(request, 'staff_details.html',
                           {'current_url': current_url,
                            'person': person,
                            'staff_list': staff_list,
                            'staff_id': staff_id,
                            'person': person,
                            'physician': physician
                            })


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


def Remove_Physician(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffid', None)
        p = get_object_or_404(Physician, pk=staff_id)
        p.delete()
    return redirect('Remove_MedStaff')


def Remove_Nurse(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffid', None)
        p = get_object_or_404(Nurse, pk=staff_id)
        p.delete()
    return redirect('Remove_MedStaff')


def Remove_Surgeon(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffid', None)
        p = get_object_or_404(Surgeon, pk=staff_id)
        p.delete()
    return redirect('Remove_MedStaff')


def Add_Physician(request):
    title = 'New Physician Form'
    form1 = NewPersonForm()
    form2 = NewPhysicianForm()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form1 = NewPersonForm(request.POST)
        form2 = NewPhysicianForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            person = form1.save()
            p = form2.save(commit=False)
            p.person = person
            p.save()
            return redirect('Staff_Details', staff_id=p.pk)
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
            p = form2.save(commit=False)
            p.person = person
            p = form2.save()
            return redirect('Staff_Details', staff_id=p.pk)
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
            p = form2.save(commit=False)
            p.person = person
            p = form2.save()
            return redirect('Staff_Details', staff_id=p.pk)
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
            p = form2.save(commit=False)
            p.person = person
            p = form2.save()
            return redirect('Staff_Details', staff_id=p.pk)
    forms = []
    forms.append(form1)
    forms.append(form2)
    return render(request, 'new_staff.html', {'forms': forms,
                                              'current_url': current_url,
                                              'title': title})


def Add_Chief(request):
    form = NewChiefForm()
    title = "Add a Dept Chief Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewChiefForm(request.POST)
        if form.is_valid():
            form.save()
    thing_list = Chief.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def Add_Illness_Type(request):
    title = "Add an Illness_Type to Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewIllness_TypeForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewIllness_TypeForm()
    thing_list = Illness_Type.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddMed(request):
    title = "Add Medication to Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewMedForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewMedForm()
    thing_list = Medication.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddMedInt(request):
    title = "Add Drug Interaction to Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewMedIntForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewMedIntForm()
    thing_list = Medication_Interaction.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddContract(request):
    title = "Add Contract to Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewContractForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewContractForm()
    thing_list = Contract.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddSkill(request):
    title = "Add Skills to Hospital"
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewSkillForm()
    thing_list = Skill.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddTheater(request):
    current_url = request.get_full_path()
    title = "Add Theaters to Hospital"
    if request.method == 'POST':
        form = NewTheaterForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewTheaterForm()
    thing_list = Theater.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddCorp(request):
    current_url = request.get_full_path()
    title = "Add Corporations to Hospital"
    if request.method == 'POST':
        form = NewCorpForm(request.POST)
        if form.is_valid():
            form.save()
    form = NewCorpForm()
    thing_list = Corporation.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def AddSurgeryType(request):
    current_url = request.get_full_path()
    title = "Add Surgery Type to Hospital"
    if request.method == 'POST':
        form = NewSurgeryTypeForm(request.POST)
        if form.is_valid():
            form.save()

    form = NewSurgeryTypeForm()
    thing_list = Surgery_Type.objects.all()
    return render(request, 'add.html', {'form': form,
                                        'current_url': current_url,
                                        'thing_list': thing_list,
                                        'title': title})


def Schedule_MedStaff(request):
    form = Schedule_MedStaffStep1()
    current_url = request.get_full_path()
    title = 'Step1: Select Staff Type'
    step = 'step1'
    if request.method == 'POST':
        if 'step1' in request.POST:
            form = Schedule_MedStaffStep1(request.POST)
            if form.is_valid():
                step = 'step2'
                title = 'Step2: Select Staff and Date'
                staff_id = request.POST.get('staff_type', None)
                staff_type = ContentType.objects.get(pk=staff_id)
                staff_type = staff_type.model_class()

                form = Schedule_MedStaffForm(staff_type=staff_type)

                return render(request, 'schedule.html',
                              {'form': form,
                               'current_url': current_url,
                               'step': step,
                               'title': title
                               })

        if 'step2' in request.POST:
            staffer = request.POST.get('staffer', None)
            content_id = request.POST.get('content_id', None)
            time = request.POST['time'].split(':')
            content_id = ContentType.objects.get(pk=content_id)
            s = Schedule()
            s.content_type = content_id
            s.object_id = staffer
            s.shift = datetime.datetime(
                    day=int(request.POST['shift_day']),
                    month=int(request.POST['shift_month']),
                    year=int(request.POST['shift_year']),
                    hour=int(time[0]),
                    minute=int(time[1])
                    )
            s.save()
            return redirect('Schedule_MedStaff')

    appointments = Schedule.objects.all()
    return render(request, 'schedule.html', {'form': form,
                                             'current_url': current_url,
                                             'title': title,
                                             'appointments': appointments,
                                             'step': step})
