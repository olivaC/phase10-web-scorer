from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from game.forms import LoginForm, UserCreateForm
from game.utils import unquote_redirect_url
from phase10Scorer.settings import PASSWORD


@login_required
def index(request):
    return render(request, 'index.html')


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
