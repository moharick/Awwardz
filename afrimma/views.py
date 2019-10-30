from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import datetime as dt
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.


def convert_dates(dates):
    # function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday',
            'thursday', 'Friday', 'Saturday', 'Sunday']
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
            return redirect('home', context_instance=RequestContext(request))
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'profile': profile})


@login_required(login_url='/accounts/login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user=current_user)
    print(profile)
    projects = Project.objects.filter(user=current_user)
    my_profile = Profile.objects.get(user=current_user)
    return render(request, 'profile.html', locals())


@login_required(login_url='/accounts/login')
def project(request, project_id):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise ObjectDoesNotExist()

    total_design = 0
    total_usability = 0
    total_content = 0
    overall_score = 0

    ratings = Review.objects.filter(project=project_id)
    if len(ratings) > 0:
        users = len(ratings)
    else:
        users = 1

    design = list(Review.objects.filter(
        project=project_id).values_list('design', flat=True))
    usability = list(Review.objects.filter(
        project=project_id).values_list('usability', flat=True))
    content = list(Review.objects.filter(
        project=project_id).values_list('content', flat=True))

    total_design = sum(design)/users
    total_usability = sum(usability)/users
    total_content = sum(content)/users

    overall_score = (total_design+total_content+total_usability)/3

    project.design = total_design
    project.usability = total_usability
    project.content = total_content
    project.overall = overall_score
    project.save()

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project = project
            rating.profile = profile
            if not Review.objects.filter(profile=profile, project=project).exists():
                rating.overall_score = (
                    rating.design+rating.usability+rating.content)/3
                rating.save()
    else:
        form = ReviewForm()
    return render(request, "review.html", {"project": project, "profile": profile, "ratings": ratings, "form": form, 'total_design': total_design, 'total_usability': total_usability, 'total_content': total_content})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = current_user
            prof.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm()
    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url='/accounts/login')
def search(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        projects = Project.search_project(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "projects": projects, 'profile': profile})
    else:
        message = "Please enter search term"
        return render(request, 'search.html', {"message": message, "projects": projects, 'profile': profile})

def logout(request):
    return redirect('home.html')

class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDescription(APIView):

    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)


class ProjectDescription(APIView):

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)