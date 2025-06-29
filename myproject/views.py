from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import re
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            
            if re.match(r'^\d{2}p-\d{4}$', username):  
                return redirect('dashboard')  # Redirect to student portal
            else:
                return redirect('teacherdashboard')  # Redirect to teacher portal

        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')
