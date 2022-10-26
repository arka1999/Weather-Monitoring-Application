from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages 
from django.contrib.auth.models import User 


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home(request):
    return render(request,'authentication.html')

def show_data(request):
    return render(request,'index.html')



def data_from_thingspeak(request,template_name='data_from_thingspeak.html'):
    return render(request,template_name)

def fetch_datafrom_thingspeak(request):
    import urllib
    import json
    data = {}
    sensor_data = []
    if is_ajax(request):
        now = datetime.now()
        ok_date = (str(now.strftime('%Y-%m-%d %H:%M:%S')))
        custom_url = request.GET.get('id', None)
        try:
            with urllib.request.urlopen(custom_url) as url:
                s = url.read()
                data = json.loads(s)
            if data:
                sensor_data = {
                    'date': str(ok_date),
                    'temp': data['feeds'][1]['field1'],
                    'humidity': data['feeds'][1]['field2'],}
            else:
                sensor_data = {
                    'date': str(ok_date),
                    'temp': 'No Data',
                    'humidity': 'No Data',}
        except Exception as x:
            sensor_data = {
                'date': str(ok_date),
                'temp': 'Network Error',
                'humidity': 'Network Error',}
        

        data['result'] = sensor_data
    else:
        data['result'] = "Not Ajax"
        
    return JsonResponse(data)
    
def live_data(request):
    import requests
    response = requests.get('https://api.thingspeak.com/channels/1758870/feeds.json?api_key=5X7V8TFH88X86K86&results=2')
    data = response.json()
    city_weather={
            'temparature':data['feeds'][0]['field1'],
            'humidity':data['feeds'][0]['field2'],
    }

    return render(request,'live.html',{'city_weather':city_weather})      


def graph_from_thingspeak(request,template_name='graph_from_thingspeak.html'):
    return render(request,template_name)
  

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST.get('pass1')
        pass2=request.POST['pass2']

        # check for errorneous input
        if not len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('Student:home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('Student:home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('Student:home')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        return render(request,'index.html', {'messages':messages})

    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            return redirect("Student:show_data")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("Student:home")

    return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Student:home')

import pandas as pd

    
# Dataset Uses

def query(request,template_name='query.html'):
    
    def cal():
        if request.method == "POST":
            # Get the post parameters
            temp=request.POST['temp']
            temp = int(temp)
            
            url='https://drive.google.com/file/d/1bunQmOn82fcldEna9IG7wMejoLk1ue2T/view?usp=sharing'
            url='https://drive.google.com/uc?id=' + url.split('/')[-2]
            data = pd.read_csv(url)
            x=data[['created_at','field1']]
            p=x.loc[x.field1>temp]
            freq = p.to_html()
            return(freq)
    context={}
    context['calculated_value'] = cal()
    
    
    
    return render(request, template_name, context)

    

