from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from game.forms import LoginForm, UserCreateForm, NewGameForm
from game.models import Game, Score
from game.utils import unquote_redirect_url
from phase10Scorer.settings import PASSWORD


@login_required
def index(request):
    context = dict()
    games = Game.objects.all().filter(finish=False)
    game_list = []
    if games:
        for game in games:
            if game.players.filter(pk=request.user.pk).exists():
                game_list.append(game)

    context['games'] = game_list
    return render(request, 'index.html', context)


def login_view(request):
    """
    Login page.

    :param request:
    :return:
    """
    context = dict()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=PASSWORD)
                login(request, user)
                redirect_url = request.POST.get('next', reverse("game:index"))
                return HttpResponseRedirect(unquote_redirect_url(redirect_url))
            else:
                context['next'] = unquote_redirect_url(request.GET.get('next', reverse("game:index")))
        except:
            context['next'] = unquote_redirect_url(request.GET.get('next', reverse("game:index")))

    else:
        context['next'] = request.GET.get('next', '')
        form = LoginForm()
    context['form'] = form
    # context['path'] = settings.DOMAIN
    return render(request, 'login.html', context)


def register_view(request):
    """
    Allows a new author to register.

    :param request:
    :return:
    """
    context = dict()
    if request.method == 'POST':
        next = request.POST.get("next", reverse("game:index"))
        form = UserCreateForm(request.POST)
        try:
            if form.is_valid():
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    password='phase10123'
                )
                user.save()
                user = authenticate(username=user.username, password=PASSWORD)
                login(request, user)
                return HttpResponseRedirect(reverse('game:index'))
            else:
                messages.success(request,
                                 'Sign up error')

            context['next'] = next
        except:
            context['next'] = request.GET.get('next', reverse("game:index"))
    else:
        form = UserCreateForm()
        context['next'] = request.GET.get('next', reverse("game:index"))
    context['form'] = form
    return render(request, 'register.html', context)


@login_required
def logout_view(request):
    """
    View used for logging out.

    :param request:
    :return: The index page.
    """
    logout(request)
    return HttpResponseRedirect(request.GET.get(next, reverse("game:index")))


@login_required
def new_game(request):
    context = dict()
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.create(
                name=form.cleaned_data['name'].strip()
            )
            user = request.user
            game.players.add(user)
            game.save()
            Score.objects.create(
                player=user,
                game=game
            )
            return HttpResponseRedirect(game.get_url())

    form = NewGameForm()
    context['form'] = form
    return render(request, 'new_game.html', context)


@login_required
def game(request, name):
    game = Game.objects.get(name__exact=name)
    user = request.user

    try:
        player = game.players.all().get(username=user.username)
        score = Score.objects.get(player=user, game=game)
        scores = Score.objects.all().filter(game=game).order_by('phase')
    except:
        score = None
        print("No score for this player")

    players = game.players.all()

    return render(request, 'game.html', locals())


@login_required
def search_view(request):
    context = dict()
    query = request.GET.get("q")

    if query:
        queryset = Game.objects.all().filter(finish=False, name__icontains=query)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context['games'] = queryset

    return render(request, 'search_games.html', context)


@login_required
def join_game(request):
    query = request.GET.get("q")
    game = Game.objects.get(id=query)
    user = request.user
    game.players.add(user)
    game.save()
    Score.objects.create(
        player=user,
        game=game
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def start_game(request):
    query = request.GET.get("q")
    game = Game.objects.get(id=query)
    if game:
        game.start = True
        game.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_score(request):
    score = request.GET.get("score")
    phase = request.GET.get("phase")
    query = request.GET.get("q")
    player = request.GET.get("p")

    game = Game.objects.get(id=query)

    if game.finish:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    s = Score.objects.get(game=game, player_id=player)
    s.score = int(score)
    s.phase = int(phase)
    s.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_round(request):
    query = request.GET.get("q")
    game = Game.objects.get(id=query)
    if game.finish:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if game:
        game.round += 1
        game.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def finish_game(request):
    query = request.GET.get("q")
    game = Game.objects.get(id=query)
    if game:
        game.finish = True
        game.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
