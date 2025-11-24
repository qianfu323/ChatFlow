import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse


def user_login(request):
    """
    login function
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'Please enter both username and password'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def user_register(request):
    """
    register function
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if username and password:
            user = User.objects.create_user(username=username, password=password, email=email)
            if user is not None:
                return JsonResponse({'success': True, 'message': 'Registration successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Registration failed'})
        else:
            return JsonResponse({'success': False, 'message': 'Please enter both username and password'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})
