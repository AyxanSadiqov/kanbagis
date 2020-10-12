# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

class RegisterPageSlide(models.Model):
    header = models.CharField(max_length=32)
    image = models.FileField(upload_to='', help_text="640x426")
    created_at = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    def __str__(self):
        return self.header

class province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=100,help_text="İl :")

    def __str__(self):
        return self.province_name

class county(models.Model):
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=100,help_text="İlçe :")
    province_id = models.ForeignKey(province, on_delete=models.CASCADE, help_text="İl :")

    def __str__(self):
        return  self.county_name

class blood_group(models.Model):
    blood_id = models.AutoField(primary_key=True)
    blood_name = models.CharField(max_length=32,help_text="Kan Grubu :")

    def __str__(self):
        return self.blood_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, null=True, max_length=20)
    blood_group = models.ForeignKey(blood_group, on_delete=models.CASCADE,blank=True, null=True,help_text="Kan Grubu :")
    province = models.ForeignKey(province, on_delete=models.CASCADE,blank=True, null=True,help_text="İl :")
    county = models.ForeignKey(county, on_delete=models.CASCADE,blank=True, null=True,help_text="İlçe :")
    birth_date = models.DateTimeField(blank=True, null=True,default=datetime.now)
    created_at = models.DateTimeField(blank=True, null=True,auto_now_add = True)
    updated_at = models.DateTimeField(blank=True, null=True,auto_now = True)
    confirmed = models.BooleanField(default=False, help_text="Onaylı kullanıcı")
    privacy = models.BooleanField(default=False, help_text="Gizlilik")
    informed = models.BooleanField(default=False, help_text="Bilgili kullanıcı")

    def __str__(self):
        return self.user.username

BLOOD_CHOICES = (
   ('kan arıyor', 'Kan arıyorum'),
   ('kan veriyor', 'Kan veriyorum')
)

class blood_share(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    blood_group = models.ForeignKey(blood_group, on_delete=models.CASCADE,help_text="Kan Grubu :")
    province = models.ForeignKey(province, on_delete=models.CASCADE,help_text="İl :")
    county = models.ForeignKey(county, on_delete=models.CASCADE,help_text="İlçe :")
    date_range = models.DateTimeField(default=datetime.now,help_text="Tarih aralığı :")
    searching_reason = models.TextField(max_length=700,editable = True,help_text="Kan arama nedeni :")
    contact_name = models.CharField(max_length=32,help_text="İletişim ismi :")
    contact_number = models.CharField(max_length=20,help_text="İletişim numarası :")
    choice = models.CharField(choices=BLOOD_CHOICES,max_length=32)
    sharing_date = models.DateTimeField(blank=True, null=True,auto_now_add = True)
    updated_at = models.DateTimeField(blank=True, null=True,auto_now = True)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True)

    def __str__(self):
        return self.user.username

NOTIFICATION_TYPE = (
    ('info', 'Bilgi'),
    ('success', 'Başarılı'),
    ('alert', 'Uyarı')
)

class ProfileNotification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=32)
    body = models.TextField(max_length=500, editable = True)
    footer = models.CharField(max_length=32)
    choice = models.CharField(choices=NOTIFICATION_TYPE,max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.header
        # return ("{0} {1} {2}".format(self.receiver, self.header, self.choice))

class HomeRightInformation(models.Model):
    content = models.TextField(max_length=150)
    written_by = models.CharField(max_length=16)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    message = models.TextField(max_length=700,editable = True)
    created_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="receiver")
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.message

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(blank=True, null=True, max_length=225)
    status = models.CharField(blank=True, null=True, max_length=225)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user,
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False

class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_thread_first")
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_thread_second")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'Oda-{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False

    def __str__(self):
        return str(self.first) if self.first else ''

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='sender')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
