from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.urls import reverse

from game.forms import LoginForm, UserCreateForm, NewGameForm
from game.models import Game, Score
from game.utils import unquote_redirect_url
from phase10Scorer.settings import PASSWORD

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]

mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''

    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser


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
    if mobileBrowser(request):
        return render(request, 'mobile/index.html', context)
    else:
        return render(request, 'desktop/index.html', context)


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
            try:
                game_check = Game.objects.get(name__iexact=form.cleaned_data['name'])
                if game_check:
                    messages.error(request,
                                   'Game name already taken. Try again.')
                    if mobileBrowser(request):
                        return render(request, 'mobile/new_game.html', context)
                    else:
                        return render(request, 'desktop/new_game.html', context)
            except:
                print("All good")

            game = Game.objects.create(
                name=form.cleaned_data['name'].strip()
            )
            user = request.user
            game.players.add(user)
            game.host = user
            game.save()
            Score.objects.create(
                player=user,
                game=game
            )
            return HttpResponseRedirect(game.get_url())

    form = NewGameForm()
    context['form'] = form
    if mobileBrowser(request):
        return render(request, 'mobile/new_game.html', context)
    else:
        return render(request, 'desktop/new_game.html', context)


@login_required
def game(request, id):
    game = Game.objects.get(id__exact=id)
    user = request.user
    score_list = list()

    try:
        player = game.players.all().get(username=user.username)
        score = Score.objects.get(player=user, game=game)
        scores = Score.objects.all().filter(game=game).order_by('-phase')
        players = game.players.all()
        _index = 0

        for s in scores:
            if score_list:
                for l in score_list:
                    if s.phase < l.phase:
                        _index = score_list.index(l) + 1
                    if s.phase == l.phase and s.score >= l.score:
                        _index = score_list.index(l) + 1
                    if s.phase == l.phase and s.score <= l.score:
                        _index = score_list.index(l)
                score_list.insert(_index, s)
            else:
                score_list.append(s)
            if s not in score_list:
                score_list.append(s)

        scores = score_list
        players = game.players.all()
    except:
        score = None
        print("No score for this player")

    players = game.players.all()

    if mobileBrowser(request):
        return render(request, 'mobile/game.html', locals())
    else:
        return render(request, 'desktop/game.html', locals())


@login_required
def search_view(request):
    context = dict()
    query = request.GET.get("q").strip()

    if query:
        queryset = Game.objects.all().filter(finish=False, name__icontains=query)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context['games'] = queryset
    if mobileBrowser(request):
        return render(request, 'mobile/search_games.html', context)
    else:
        return render(request, 'desktop/search_games.html', context)


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
    addsub = request.GET.get("addsub")
    score = request.GET.get("score")
    phase = request.GET.get("phase")
    query = request.GET.get("q")
    player = request.GET.get("p")

    game = Game.objects.get(id=query)

    if game.finish:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    s = Score.objects.get(game=game, player_id=player)
    if addsub == "add":
        s.score += int(score)
    else:
        s.score -= int(score)
    if phase:
        s.phase += 1
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
    winner = request.GET.get("w")
    game = Game.objects.get(id=query)
    score = Score.objects.get(game=game, player_id=winner)
    score.winner = True
    score.save()
    if game:
        game.finish = True
        game.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def go_back(request):
    x = 'yar'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
