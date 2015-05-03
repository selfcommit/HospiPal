from django.db import models


class Person(models.Model):
    ssn = models.IntegerField(unique=True)

    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    first_name = models.CharField(max_length=33)
    last_name = models.CharField(max_length=33)
    street1 = models.CharField(max_length=255, blank=False)
    street2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    zipcode = models.CharField(max_length=255, blank=False)
    telephone = models.CharField(max_length=33, blank=False)

    def _get_full_name(self):
        "Returns the Full Person Name"
        return '%s %s' % (self.first_name, self.last_name)

    name = property(_get_full_name)

    def __unicode__(self):
        return self.name


class SupportStaff(models.Model):
    person = models.ForeignKey(Person)
    salary_amount = models.IntegerField(blank=True, null=True)

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return 'staff %s' % (self.person)


class Skill(models.Model):
    name = models.CharField(max_length=33, blank=False)

    def __unicode__(self):
        return self.name


class Surgeon(models.Model):
    person = models.OneToOneField(Person, primary_key=True)
    skills = models.ManyToManyField(Skill)
    salary_amount = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return 'Surgeon %s' % str(self.person)


class Physician(models.Model):
    person = models.OneToOneField(Person, primary_key=True)
    skill = models.ForeignKey(Skill)
    ownership = models.BooleanField(default=False)
    salary_amount = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return 'Physician %s' % str(self.person)


class Nurse(models.Model):
    person = models.OneToOneField(Person, primary_key=True)
    years_experience = models.IntegerField('Years of Experience')
    skill = models.ForeignKey(Skill)
    grade = models.CharField(max_length=1)
    salary_amount = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return 'Nurse %s' % str(self.person)


class Chief(models.Model):
    physician = models.ForeignKey(Physician)
    dept = models.CharField(max_length=33)

    def __unicode__(self):
        return 'Chief %s of %s' % (self.physician, self.dept)


class Theater(models.Model):
    name = models.CharField(max_length=33, blank=False)

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name


class NursingUnit(models.Model):
    UNIT_CHOICE = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
        (6, 'Six'),
        (7, 'Seven'),
    )
    number = models.IntegerField(choices=UNIT_CHOICE)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Unit %s' % (self.number)


class NursingRoom(models.Model):
    ROOM_CHOICE = (
        ('Blue', 'Blue'),
        ('Green', 'Green'),
    )
    unit = models.ForeignKey(NursingUnit)
    color = models.CharField(max_length=5, choices=ROOM_CHOICE)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s Room %s' % (self.unit, self.color)


class Bed(models.Model):
    BED_CHOICE = (
        ('A', 'Bed A'),
        ('B', 'Bed B'),
    )
    room = models.ForeignKey(NursingRoom)
    letter = models.CharField(max_length=1, choices=BED_CHOICE)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Unit %s Room %s Bed %s' % (self.room.unit.number,
                                           self.room.color, self.letter)


class Patient(models.Model):
    person = models.OneToOneField(Person, primary_key=True)
    primary = models.ForeignKey(Physician)
    hdl = models.CharField(max_length=33)
    ldl = models.CharField(max_length=33)
    tri = models.CharField(max_length=33)
    blood_sugar = models.CharField(max_length=33)
    needs_surgery = models.BooleanField(default=False)
    date_admitted = models.DateTimeField('date_admitted', auto_now_add=True, editable=False)
    date_discharged = models.DateTimeField(blank=True, null=True)
    attending_nurse = models.ForeignKey(Nurse, null=True)
    bed = models.ForeignKey(Bed, blank=True, null=True)

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def _get_location(self):
        "Returns Patient Location"
        return '%s %s %s' % (self.nursing_unit, self.room_number, self.bed_label)

    def __unicode__(self):
        return 'Patient %s' % (str(self.person))


class Illness_Type(models.Model):
    name = models.CharField(max_length=33, blank=False)
    ILLNESS_CHOICE = (
        ('A', 'Allergie'),
        ('D', 'Disease'),
    )
    category = models.CharField(max_length=1, choices=ILLNESS_CHOICE)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Illness(models.Model):
    name = models.ForeignKey(Illness_Type, related_name='name_of_illness')
    patient = models.ForeignKey(Patient)
    date_added = models.DateTimeField('date_added',
                                      auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.patient, self.date_added)


class Surgery_Type(models.Model):
    name = models.CharField(max_length=33, blank=False)

    CATEGORY_CHOICE = (
        ('H', 'Hospitalization'),
        ('O', 'Outpatient'),
    )
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICE)
    anatomical_location = models.CharField(max_length=33)
    special_needs = models.CharField(max_length=33)
    skills = models.ManyToManyField(Skill, related_name='skills_for_surgerytype')

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name


class Surgery(models.Model):
    surgery_type = models.ForeignKey(Surgery_Type)
    date_performed = models.DateTimeField()
    nurses = models.ManyToManyField(Nurse)
    surgeons = models.ManyToManyField(Surgeon)
    patient = models.ForeignKey(Patient, related_name='patients_in_surgery')
    theater = models.ForeignKey(Theater, related_name='theater_of_surgery')

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s to operate on %s in %s' % (self.surgeons.all(), self.patient, self.theater)


class Consultation(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Physician)
    date_of_consult = models.DateTimeField()

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s with %s at %s' % (self.patient, self.doctor, self.date_of_consult.strftime('%H:%M'))


class Medication(models.Model):
    name = models.CharField(max_length=33, blank=False)
    quantity_on_hand = models.IntegerField()
    quantity_on_order = models.IntegerField()
    unit_cost = models.IntegerField()
    year_to_date = models.DateTimeField('year_to_date', auto_now_add=True, editable=False)
    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name


class Medication_Interaction(models.Model):
    prescribed_drug = models.ForeignKey(Medication, related_name='prescribed_drug')
    interfering_drug = models.ForeignKey(Medication, related_name='interfering_drug')
    INTERACTION_CHOICE = (
        ('S', 'Severe interaction'),
        ('M', 'Moderate interaction'),
        ('L', 'Little interaction'),
        ('N', 'No interaction'),
    )
    interaction = models.CharField(max_length=1, choices=INTERACTION_CHOICE)

    def __unicode__(self):
        return '%s interfers with %s' % (self.prescribed_drug, self.interfering_drug)


class Prescription(models.Model):
    medication = models.ForeignKey(Medication)
    prescriber = models.ForeignKey(Physician)
    patient = models.ForeignKey(Patient)
    diagnosis = models.ManyToManyField(Illness)
    dosage = models.CharField(max_length=33, blank=False)
    frequency = models.CharField(max_length=33, blank=False)
    consultation = models.ForeignKey(Consultation)

    date_added = models.DateTimeField('date_added', auto_now_add=True, editable=False)
    date_updated = models.DateTimeField('date_updated', auto_now_add=True, editable=False)

    def __unicode__(self):
        return '%s prescribed for %s %s %s on %s' %(self.medication, self.patient, self.dosage, self.frequency, self.date_added)


class Contract(models.Model):
    surgeon = models.ForeignKey(Surgeon)
    skills = models.ManyToManyField(Skill)
    years = models.IntegerField('Term of Contract in years')


class Corporation(models.Model):
    name = models.CharField(max_length=33, blank=False, unique=True)
    headquarters = models.CharField(max_length=33, blank=False)
    percent = models.IntegerField()
