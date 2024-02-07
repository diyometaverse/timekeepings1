from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from newapp.models import Time
from datetime import datetime

def home_view(request):
    user = request.user
    latest_time_entry = None
    error_message = None

    try:
        time_out_entry = Time.objects.filter(user=user, time_out=None).latest('time_in')
        return redirect('newapp:landingpage')
    except Time.DoesNotExist:
        pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            action = request.POST.get('action')

            if action == 'time_out':
                try:

                    time_in_entry = Time.objects.filter(user=user, time_out=None).latest('time_in')
                    time_in_entry.time_out = datetime.now()
                    time_in_entry.save()
                    return redirect('newapp:landingpage')
                except Time.DoesNotExist:
                    error_message = "You haven't done a time-in yet."

            request.POST = None

        try:
            latest_time_entry = Time.objects.filter(user=user).latest('time_in')
        except Time.DoesNotExist:
            latest_time_entry = None

    return render(request, 'home.html', {'latest_time_entry': latest_time_entry, 'error_message': error_message})
