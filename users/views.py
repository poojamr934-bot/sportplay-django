from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile
        Profile.objects.create(
            user=user,
            gender=gender
        )

        return redirect('register')  # temporary redirect

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')

from .models import Game

def game_list(request):
    query = request.GET.get('q')
    
    if query:
        games = Game.objects.filter(name__icontains=query)
    else:
        games = Game.objects.all()

    popular_games = Game.objects.annotate(
        total_players=Count('gameregistration')).order_by('-total_players')[:3]

    return render(request, 'users/game_list.html', {
        'games': games,
        'query': query,
        'popular_games': popular_games
    })

   
from .models import Game, GameRegistration

def game_detail(request, id):
    game = get_object_or_404(Game, id=id)

    registered = False
    if request.user.is_authenticated:
        registered = GameRegistration.objects.filter(
            user=request.user,
            game=game
        ).exists()

    return render(request, 'users/game_detail.html', {
        'game': game,
        'registered': registered,
    })

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import GameRegistration

@login_required
def register_game(request, id):
    game = Game.objects.get(id=id)

    # check if user already registered
    already_registered = GameRegistration.objects.filter(
        user=request.user,
        game=game
    ).exists()

    if not already_registered:
        GameRegistration.objects.create(
            user=request.user,
            game=game
        )

    return redirect('game_detail', id=game.id)

@login_required
def my_games(request):
    registrations = GameRegistration.objects.filter(user=request.user)

    return render(request, 'users/my_games.html', {
        'registrations': registrations
    })

from django.shortcuts import redirect, get_object_or_404
from .models import GameRegistration

def cancel_registration(request, reg_id):
    registration = get_object_or_404(GameRegistration, id=reg_id, user=request.user)
    registration.delete()
    return redirect('my_games')