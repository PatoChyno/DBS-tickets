# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

class Actor(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        db_table = 'actor'

    def __str__(self):
        return self.name
    
class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Customer(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(blank=True, null=True)
    event = models.CharField(max_length=100, blank=True)
    adults = IntegerRangeField(min_value=0, blank=True)
    students = IntegerRangeField(min_value=0, blank=True)
    children = IntegerRangeField(min_value=0, blank=True)
    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name

class BuyTicketForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'birthday', 'gender', 'phone', 'event', 'adults', 'students', 'children']

class PricesForm(models.Model):
    event = models.CharField(max_length=100, blank=True)
    adults = IntegerRangeField(min_value=0, blank=True)
    students = IntegerRangeField(min_value=0, blank=True)
    children = IntegerRangeField(min_value=0, blank=True)
    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.event

class UpdatePricesForm(ModelForm):
    class Meta:
        model = PricesForm
        fields = ['event', 'adults', 'students', 'children']

class EventForm(models.Model):
    event = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'event_edition'

    def __str__(self):
        return self.event

class DeleteEventForm(ModelForm):
    class Meta:
        model = EventForm
        fields = ['event']

class DatePrice(models.Model):
    category = models.CharField(max_length=20)
    price = models.FloatField()
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    edition = models.ForeignKey('EventEdition')
    class Meta:
        db_table = 'date_price'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    id = models.IntegerField(primary_key=True)
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class Event(models.Model):
    name = models.CharField(max_length=30)
    established = models.DateField(blank=True, null=True)
    organizer = models.ForeignKey('Organizer')
    category = models.ForeignKey('EventCategory')
    class Meta:
        db_table = 'event'

class EventCategory(models.Model):
    label = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = 'event_category'

class EventEdition(models.Model):
    label = models.CharField(max_length=30, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendance = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey('Event')
    venue = models.ForeignKey('Venue')
    class Meta:
        db_table = 'event_edition'

class Organizer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'organizer'

class Performing(models.Model):
    salary = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    label = models.CharField(max_length=30, blank=True)
    edition = models.ForeignKey(EventEdition)
    actor = models.ForeignKey(Actor)
    class Meta:
        db_table = 'performing'

class Ticket(models.Model):
    category = models.CharField(max_length=20, blank=True)
    pieces = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    order = models.ForeignKey('TicketOrder')
    class Meta:
        db_table = 'ticket'

class TicketOrder(models.Model):
    buy_date = models.DateTimeField()
    customer = models.ForeignKey(Customer)
    edition = models.ForeignKey(EventEdition)
    class Meta:
        db_table = 'ticket_order'

class Venue(models.Model):
    label = models.CharField(max_length=30)
    capacity = models.IntegerField()
    class Meta:
        db_table = 'venue'
