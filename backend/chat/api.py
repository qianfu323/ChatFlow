import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Room, Message


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


def room(request):
    """
    chat room handler
    :param request:
    :return:
    """
    if request.method == 'GET':
        # List all rooms or get a specific room by ID
        try:
            room_id = request.GET.get('id')
            if room_id:
                # Get specific room
                room = Room.objects.get(id=room_id)
                return JsonResponse({
                    'success': True,
                    'data': {
                        'id': room.id,
                        'name': room.name,
                        'last_message_at': room.last_message_at,
                        'is_private': room.is_private
                    }
                })
            else:
                # List all rooms
                rooms = Room.objects.all()
                rooms_data = [{
                    'id': room.id,
                    'name': room.name,
                    'last_message_at': room.last_message_at,
                    'is_private': room.is_private
                } for room in rooms]
                return JsonResponse({
                    'success': True,
                    'data': rooms_data
                })
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Room not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    elif request.method == 'POST':
        # Create new room
        try:
            data = json.loads(request.body)
            name = data.get('name', '')

            if not name:
                return JsonResponse({'success': False, 'message': 'Room name is required'})

            is_private = data.get('is_private', False)

            room = Room.objects.create(
                name=name,
                is_private=is_private
            )

            return JsonResponse({
                'success': True,
                'message': 'Room created successfully',
                'data': {
                    'id': room.id,
                    'name': room.name,
                    'last_message_at': room.last_message_at,
                    'is_private': room.is_private
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    elif request.method == 'PUT':
        # Update existing room
        try:
            data = json.loads(request.body)
            room_id = data.get('id')

            if not room_id:
                return JsonResponse({'success': False, 'message': 'Room ID required'})

            if not data.get("name"):
                return JsonResponse({'success': False, 'message': 'Room name is required'})

            room = Room.objects.get(id=room_id)
            room.name = data.get('name', room.name)
            room.is_private = data.get('is_private', room.is_private)
            room.save()

            return JsonResponse({
                'success': True,
                'message': 'Room updated successfully',
                'data': {
                    'id': room.id,
                    'name': room.name,
                    'last_message_at': room.last_message_at,
                    'is_private': room.is_private
                }
            })
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Room not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    elif request.method == 'DELETE':
        # Delete room
        try:
            room_id = request.GET.get('id')

            if not room_id:
                return JsonResponse({'success': False, 'message': 'Room ID required'})

            room = Room.objects.get(id=room_id)
            room.delete()

            return JsonResponse({
                'success': True,
                'message': 'Room deleted successfully'
            })
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Room not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def message(request):
    """
    message handler
    :param request:
    :return:
    """
    if request.method == 'GET':
        # get messages with room id
        room_id = request.GET.get('room_id')
        if room_id:
            messages = Message.objects.filter(room_id=room_id)
            messages_data = [{
                'id': message.id,
                'room_id': message.room.id,
                'sender_id': message.sender.id,
                'username': message.sender.username,
                'message': message.content,
                'timestamp': message.timestamp
            } for message in messages]
            return JsonResponse({
                'success': True,
                'data': messages_data
            })
        else:
            return JsonResponse({'success': False, 'message': 'Room ID required'})
