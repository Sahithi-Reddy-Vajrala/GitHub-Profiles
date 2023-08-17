from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Repository
from django.contrib.auth import get_user_model
import requests


def home(request):
    return render(request, 'accounts/home.html')
	

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required()
def update_profile(request):
    user=request.user
    username=user.username
    response=requests.get('https://api.github.com/users/'+str(username))
    if response.status_code == 200:
    	p=response.json()
    	user.profile.number_of_followers = p['followers']
    	q=requests.get('https://api.github.com/users/'+str(username)+'/repos')
    	if q.status_code == 200:
    		m=q.json()
    		Repository.objects.filter(userprofile=request.user.profile).delete()
    		for i in range(len(m)):
        		Repository.objects.create(userprofile=request.user.profile,
        		reponame=m[i]["name"],
        		stars=m[i]["stargazers_count"])
    	user.save()
    else:
        messages.warning(request,f'Server Issues,Update is not working(API rate limit exceeded)')
   
    return redirect('profile')
    

    
@login_required()   
def profile(request):
    if(request.user.profile.number_of_followers==None):
        return redirect('update_profile') 
    data= Repository.objects.filter(userprofile=request.user.profile).order_by('-stars')
    return render(request, 'accounts/profile.html',{"data":data})

@login_required()
def explore(request):
    all_users= get_user_model().objects.all()
    return render(request,'accounts/explore.html',{'all_users':all_users})

@login_required()
def user_profile(request, username):
    user = get_user_model().objects.get(username=username)
    data= Repository.objects.filter(userprofile=user.profile).order_by('-stars')
    return render(request, 'accounts/user_profile.html', {"data":data,"user":user})
