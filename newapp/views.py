from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Time
from datetime import datetime

def landingpage_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            action = request.POST.get('action')

            if action == 'time_in':
                # Check if there is a pending time-in
                if Time.objects.filter(user=user, time_out=None).exists():
                    error_message = "You have a pending time-in. Complete the previous time-in before starting a new one."
                else:
                    time_in_entry = Time(user=user, time_in=datetime.now())
                    time_in_entry.save()
                    # Redirect to home.html in the 'accounts' app
                    return redirect('accounts:home')

    return redirect('accounts:home')