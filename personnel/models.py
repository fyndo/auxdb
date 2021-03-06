from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Min, CharField, SmallIntegerField, DateField, BooleanField
from django.contrib.localflavor.us.models import USStateField,USPostalCodeField,PhoneNumberField


# Create your models here.

RANK_CHOICES = (
    ('Civilian', 
     (('APP', 'Applicant'),
      ('BTC', 'Enrolled in BTC'),
      ('QUAL', 'Approved and Qualified'),
      ('RES', 'Resigned'),
      ('DROP', 'Dropped'),
      ('DIS', 'Dismissed'))),
    ('Auxiliary',
     (('APO',    'Auxiliary Police Officer'),
      ('A/Sgt',  'Auxiliary Sergeant'),
      ('A/Lt',   'Auxiliary Lieutenant'),
      ('A/Capt', 'Auxiliary Captain'),
      ('A/DI',   'Auxiliary Deputy Inspector'),
      ('A/Insp', 'Auxiliary Inspector'),
      ('A/DC',   'Auxiliary Deputy Chief'))))

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

MARITAL_CHOICES = (('M', 'Married'), 
                   ('S', 'Single'),
                   ('D', 'Divorced'),
                   ('W', 'Widowed'))

HAIR_CHOICES = (('Blk', 'Black'), 
                ('Brn', 'Brown'),
                ('Yel', 'Yellow'),
                ('Gry', 'Grey'))

EYE_CHOICES = (('Gry', 'Grey'),
               ('Blu', 'Blue'), 
               ('Hzl', 'Hazel'), 
               ('Brn', 'Brown'),
               ('Yel', 'Yellow'),
               ('Grn', 'Green'))

def fake_idno():
    try:
        n = Person.objects.aggregate(Min('idno'))['idno__min']
    except:
        n = 0
    if n == None:
        n = 0
    if n > 0:
        n = 0
    return n-1

def valid_idno(no):
    if (no > 0 and no < 300000):
        raise ValidationError('%s too small' % no)
    if (no > 999999):
        raise ValidationError('%s too large' % no)
    if (no < -10000):
        raise ValidationError('%s too negative' % no)

class Person(models.Model):
    def __unicode__ (self):
        return self.rank + " " + self.last_name + ", " + self.first_name

    last_name    = CharField(max_length = 40)
    first_name   = CharField(max_length = 40)
    middle_name  = CharField(max_length = 40)
    rank         = CharField(max_length = 7, choices = RANK_CHOICES)
    idno         = SmallIntegerField(unique = True, 
                                     primary_key = True, 
                                     validators = [valid_idno],
                                     default=fake_idno)
    shield       = SmallIntegerField(null = True,
                                     blank = True)
    address      = CharField(max_length = 80)
    apt          = CharField(max_length = 8)
    city         = CharField(max_length = 40)
    state        = USStateField()
    zipcode      = CharField(max_length = 10)
    verified     = CharField(max_length = 40)
    phone        = PhoneNumberField()
    birthplace   = CharField(max_length = 80)
    birth_cert   = CharField(max_length = 40)
    birth_date   = DateField()
#    voter_no     = CharField(max_length = 40)
    entry_port   = CharField(max_length = 40)
    naturalize   = CharField(max_length = 40)
    green_card   = CharField(max_length = 40)
    other_proof  = CharField(max_length = 40)
    warrant_date = DateField()
    dmv_date     = DateField()
    gender       = CharField(max_length = 2, choices = GENDER_CHOICES)
    marital      = CharField(max_length = 2, choices = MARITAL_CHOICES)
    height       = CharField(max_length = 6)
    weight       = SmallIntegerField()
    hair_color   = CharField(max_length = 4, choices = HAIR_CHOICES)
    eye_color    = CharField(max_length = 4, choices = EYE_CHOICES)
    aka          = CharField(max_length = 80, default='No')
    addicted     = BooleanField()
    mental       = BooleanField()
    marks        = CharField(max_length = 80, default='None')
    defects      = CharField(max_length = 80, default='None')
    ssn          = CharField(max_length = 12)
    drivers      = CharField(max_length = 80)
    pistol       = CharField(max_length = 80, default='N/A')
    pistol_type  = CharField(max_length = 80, default='N/A')
    draft_status = CharField(max_length = 80)
    discharge    = CharField(max_length = 80, default='N/A')
    branch       = CharField(max_length = 80, default='N/A')
    applied      = BooleanField()
    summonsed    = BooleanField()
    max_grade    = CharField(max_length = 40)
    school       = CharField(max_length = 40)
    location     = CharField(max_length = 40)
    employer     = CharField(max_length = 80)
    emp_address  = CharField(max_length = 80)
    occupation   = CharField(max_length = 80)
    emp_phone    = PhoneNumberField()
    emp_length   = CharField(max_length = 40)
    next_kin     = CharField(max_length = 80)
    kin_relate   = CharField(max_length = 80)
    kin_addr     = CharField(max_length = 80)
    kin_phone    = PhoneNumberField()

ASSIGN_CHOICES   = (('P', 'Patrol'), 
                    ('A', 'Admin/Clerical'),
                    ('Aux', 'Other - Aux'),
                    ('PD', 'Other - PD'),
                    ('C', 'Ceremonial'))

class Tour(models.Model):
    def tour_length(self):
        len = self.tour_end - self.tour_start
        if (self.tour_start > self.tour_end):
            len += 24
        return len
    date         = DateField()
    person       = models.ForeignKey(Person)
    assignment   = CharField(max_length = 40)
    assign_type  = CharField(max_length = 4, choices = ASSIGN_CHOICES)
    tour_start   = models.PositiveSmallIntegerField()
    tour_end     = models.PositiveSmallIntegerField()

