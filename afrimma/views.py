from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
import datetime as dt
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def convert_dates(dates):
    # function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday','Tuesday','Wednesday','thursday','Friday','Saturday','Sunday']
    '''
    Returns the actual day of the week
    '''
    day = days[day_number]
    return day

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='/accounts/login')
def home(request):
    current_user = request.user
    projects = Project.objects.order_by('-overall').all()
    top = projects[0]
    runners = Project.objects.all()[:4]
    try:
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
    except ObjectDoesNotExist:
        return redirect('edit')
    return render(request, 'home.html', locals())

@login_required(login_url='/accounts/login')
def upload(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
            return redirect('home')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'profile': profile})