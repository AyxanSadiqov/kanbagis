from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from .forms import UserRegistrationForm, countyForm, provinceForm, UserProfileForm, blood_shareForm, UserRegistrationUpdateForm, UserProfileUpdateForm, feedbackForm, MessageForm, ComposeForm, HomeRightInformationForm
from .models import RegisterPageSlide, blood_share, Conversation, county, UserProfile, ProfileNotification, HomeRightInformation, Message, Thread, ChatMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext
from django.template import loader
from django.http import JsonResponse, HttpResponse
from pusher import Pusher
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from kanbagisapp import helpers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from django.db.models import Q
#from django.core.exceptions import PermissionDenied

# Create your views here.


def home(request):
    query_results = blood_share.objects.all().order_by('-sharing_date')
    query_results = helpers.pg_records(request, query_results, 5)
    homeRightInformation = HomeRightInformation.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        oneriler = UserProfile.objects.filter(~Q(user=request.user))
        if request.method == 'POST':
            form = feedbackForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Geri bildiriminiz gonderildi. Teşekkür ederiz!")
                return HttpResponseRedirect('/home/')
            else:
                print(form.errors)
        else:
            form = feedbackForm()
        context = {'query_results':query_results, 'form':form, 'homeRightInformation':homeRightInformation,'oneriler':oneriler}
        return render(request, 'kanbagisapp/home.html', context)
    else:
        oneriler = UserProfile.objects.order_by('created_at')
        if request.method == 'POST':
            form = feedbackForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Geri bildiriminiz gonderildi. Teşekkür ederiz!")
                return HttpResponseRedirect('/home/')
            else:
                print(form.errors)
        else:
            form = feedbackForm()
        context = {'query_results':query_results, 'form':form, 'homeRightInformation':homeRightInformation,'oneriler':oneriler}
        return render(request, 'kanbagisapp/home.html', context)

@login_required
def icerik(request, id):
    icerik = blood_share.objects.filter(id=id)
    homeRightInformation = HomeRightInformation.objects.all().order_by('-created_at')
    context = {'icerik':icerik, 'homeRightInformation':homeRightInformation}
    return render(request, 'kanbagisapp/icerik.html', context)

def hakkimizda(request):
    return render(request, 'kanbagisapp/hakkimizda.html',{})

def chat(request):
    return render(request, 'kanbagisapp/chat.html',{})

def paylasimdabulun(request):
    if request.method == 'POST':
        form = blood_shareForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            obj.user = request.user
            obj.save()
            messages.success(request, "Paylaşımınız başarılı bir şekilde oluşturuldu.")
            return HttpResponseRedirect('/home/')
        else:
            print(form.errors)
    else:
        form = blood_shareForm()
    homeRightInformation = HomeRightInformation.objects.all().order_by('-created_at')
    context = {'form': form, 'homeRightInformation':homeRightInformation}
    return render(request, 'kanbagisapp/paylasimdabulun.html', context)

def load_counties(request):
    province_id = request.GET.get('province')
    counties = county.objects.filter(province_id=province_id).order_by('county_name')
    return render(request, 'kanbagisapp/load.html', {'counties':counties})

@login_required
def profile(request, username=None):
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user
    bilgilerim = UserProfile.objects.filter(user=user)
    paylasimlarim = blood_share.objects.filter(user=user)
    paylasimSayi = blood_share.objects.filter(user=user).count()
    #count = blood_share.objects.filter(user=user).count()
    if request.method == 'POST':
        u_form = UserRegistrationUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Hesabınız güncellendi.")
            return redirect('profile', username=request.user)
    else:
        u_form = UserRegistrationUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    message = Message.objects.filter(receiver=request.user).order_by('-created_at')
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            obj = message_form.save(commit=True)
            obj.sender = request.user
            obj.receiver = user
            obj.save()
            messages.success(request, "Mesajınız kullanıcıya iletildi.")
            return redirect('profile', username=user)
        else:
            print(message_form.errors)
    else:
        message_form = MessageForm()

    homepaylasimSayi = HomeRightInformation.objects.filter(user=user).count()
    if request.method == 'POST':
        home_form = HomeRightInformationForm(request.POST)
        if home_form.is_valid():
            obj = home_form.save(commit=True)
            obj.user = request.user
            obj.save()
            messages.success(request, "Paylaşımınız yapıldı.")
            return HttpResponseRedirect('/home/')
        else:
            print(home_form.errors)
    else:
        home_form = HomeRightInformationForm()
    favorite = blood_share.objects.filter(favorite=request.user.id)
    pNotifications = ProfileNotification.objects.filter(receiver=request.user).order_by('-created_at')
    context = {'user': user, 'bilgilerim':bilgilerim, 'paylasimlarim':paylasimlarim, 'paylasimSayi':paylasimSayi, 'message':message, 'home_form':home_form, 'u_form':u_form, 'p_form':p_form, 'message_form':message_form, 'homepaylasimSayi':homepaylasimSayi, 'favorite':favorite, 'pNotifications':pNotifications}
    return render(request, 'kanbagisapp/profile.html', context)

def acil(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            messages.success(request, "Acil kayıt ile hesabınız oluşturuldu.")
            login(request)

            return render(request, 'registration/login.html', {})
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()
    context = {'form' : form, 'profile_form' : profile_form}
    return render(request, 'kanbagisapp/acil.html', context)

def login(request):
    return render(request, 'registration/login.html',{})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            messages.success(request, "Hesabınız başarılı bir şekilde oluşturuldu.")
            login(request)

            return render(request, 'registration/login.html', {})
    else:
        form = UserRegistrationForm()
        profile_form = UserProfileForm()
    slide = RegisterPageSlide.objects.all()
    context = {'form' : form, 'profile_form' : profile_form, 'slide':slide}
    return render(request, 'registration/registration.html', context)


def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html',{})

def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html',{})

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html',{})

def password_reset(request):
    return render(request, 'registration/password_reset_form.html',{})

@csrf_exempt
def broadcast(request):
    # collect the message from the post parameters, and save to the database
    message = Conversation(message=request.POST.get('message', ''), status='', user=request.user);
    message.save();
    # create an dictionary from the message instance so we can send only required details to pusher
    message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id}
    #trigger the message, channel and event to pusher
    pusher.trigger(u'a_channel', u'an_event', message)
    # return a json response of the broadcasted message
    return JsonResponse(message, safe=False)

#return all conversations in the database
def conversations(request):
    data = Conversation.objects.all()
    # loop through the data and create a new list from them. Alternatively, we can serialize the whole object and send the serialized response
    data = [{'name': person.user.username, 'status': person.status, 'message': person.message, 'id': person.id} for person in data]
    # return a json response of the broadcasted messgae
    return JsonResponse(data, safe=False)

#use the csrf_exempt decorator to exempt this function from csrf checks
@csrf_exempt
def delivered(request, id):
    message = Conversation.objects.get(pk=id);
    # verify it is not the same user who sent the message that wants to trigger a delivered event
    if request.user.id != message.user.id:
        socket_id = request.POST.get('socket_id', '')
        message.status = 'Delivered';
        message.save();
        message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id}
        pusher.trigger(u'a_channel', u'delivered_message', message, socket_id)
        return HttpResponse('ok');
    else:
        return HttpResponse('Awaiting Delivery');


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
