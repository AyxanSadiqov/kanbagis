from django.contrib import admin

from . import models
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import RegisterPageSlide, province, county, blood_group, UserProfile, blood_share, ProfileNotification, HomeRightInformation, Conversation, feedback, Message, Thread, ChatMessage

#son eylemleri silmek icin
#from django.contrib.admin.models import LogEntry
#LogEntry.objects.all().delete()

class RegisterPageSlideAdmin(admin.ModelAdmin):
    list_display = ("header","image")
    list_per_page = 10

class provinceAdmin(admin.ModelAdmin):
    list_display = ("province_id","province_name")
    list_per_page = 15
    search_fields = ["province_name",]
    list_filter = ("province_name",)
    #kayıt düzenlenmesini engellemek icin
    #def has_change_permission(self, request, obj=None):
        #return False

class countyAdmin(admin.ModelAdmin):
    list_display = ("county_id","county_name","province_id")
    list_per_page = 50
    list_filter = ("province_id",)
    search_fields = ["county_name",]
    #    kod ornekleri
    # list_display_links = ("county_name",) secili alani linklendirir
    # raw_id_fields = ("county_id",)

class blood_groupAdmin(admin.ModelAdmin):
    list_display = ("blood_id","blood_name")

class feedbackAdmin(admin.ModelAdmin):
    list_display = ("name","message","created_at")
    list_per_page = 15
    search_fields = ["name",]
    list_filter = ("created_at",)

class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender","receiver","message","created_at")
    list_per_page = 20
    autocomplete_fields = ['sender','receiver'] # must be ForeignKey or ManyToManyField
    list_filter = (("sender", admin.RelatedOnlyFieldListFilter),("receiver", admin.RelatedOnlyFieldListFilter),"created_at")

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['sender'] = request.user
        request.GET = data
        return super(MessageAdmin, self).add_view(request, form_url="", extra_context=extra_context)

class Conversation_Admin(admin.ModelAdmin):
    list_display = ("user","message","status","created_at")
    list_filter = ("created_at",)
    autocomplete_fields = ['user']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","phone","blood_group","province","county","birth_date","created_at","updated_at","confirmed","privacy","informed")
    list_per_page = 20
    search_fields = ["phone",]
    list_filter = ("blood_group","privacy",)
    autocomplete_fields = ['user','province','county']

class blood_shareAdmin(admin.ModelAdmin):
    list_display = ("user","blood_group","province","county","date_range","searching_reason","contact_name","contact_number","choice","sharing_date","updated_at")
    list_per_page = 20
    search_fields = ["searching_reason","contact_name","contact_number",]
    list_filter = ("blood_group","choice","sharing_date")
    date_hierarchy = "sharing_date"
    autocomplete_fields = ['user','province','county','favorite']
    radio_fields = {"choice": admin.VERTICAL}

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['user'] = request.user
        request.GET = data
        return super(blood_shareAdmin, self).add_view(request, form_url="", extra_context=extra_context)

class ProfileNotificationAdmin(admin.ModelAdmin):
    list_display = ("receiver","header","body","footer","choice","created_at","updated_at")
    list_per_page = 20
    autocomplete_fields = ['receiver']
    list_filter = (("receiver", admin.RelatedOnlyFieldListFilter),"choice")
    radio_fields = {"choice": admin.VERTICAL}

class HomeRightInformationAdmin(admin.ModelAdmin):
    list_display = ("content","written_by","user","created_at","updated_at")
    list_per_page = 10
    list_filter = ("created_at",)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    list_display = ("room_group_name","first","second","updated","timestamp")
    autocomplete_fields = ['first','second']
    class Meta:
        model = Thread


admin.site.register(RegisterPageSlide, RegisterPageSlideAdmin)
admin.site.register(province, provinceAdmin)
admin.site.register(county, countyAdmin)
admin.site.register(blood_group, blood_groupAdmin)
admin.site.register(feedback, feedbackAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(blood_share, blood_shareAdmin)
admin.site.register(ProfileNotification, ProfileNotificationAdmin)
admin.site.register(HomeRightInformation, HomeRightInformationAdmin)
admin.site.register(Conversation, Conversation_Admin)
admin.site.register(LogEntry)
admin.site.register(Thread, ThreadAdmin)
