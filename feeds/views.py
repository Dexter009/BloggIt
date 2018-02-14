import os

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from feeds.forms import AuthenticateForm, UserCreateForm, FeedsForm,UserEditForm, \
    ProfileEditForm
from feeds.models import Feeds, UserProfile


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        feeds_form = FeedsForm()
        user = request.user
        feedss_self = Feeds.objects.filter(user=user.id)
        feedss_buddies = Feeds.objects.filter(user__userprofile__in=user.profile.follows.all)
        feedss = feedss_self | feedss_buddies

        return render(request,
                      'buddies.html',
                      {'feeds_form': feeds_form, 'user': user,
                       'feedss': feedss,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password2')

            user_form.save()
            profile = UserProfile.objects.create(user=user_form)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/edit.html')


@login_required
def submit(request):
    if request.method == "POST":
        feeds_form = FeedsForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if feeds_form.is_valid():
            feeds = feeds_form.save(commit=False)
            feeds.user = request.user
            feeds.save()
            return redirect(next_url)
        else:
            return public(request, feeds_form)
    return redirect('/')


@login_required
def public(request, feeds_form=None):
    feeds_form = feeds_form or FeedsForm()
    feedss = Feeds.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'feeds_form': feeds_form, 'next_url': '/feedss',
                   'feedss': feedss, 'username': request.user.username})


def get_latest(user):
    try:
        return user.feeds_set.order_by('-id')[0]
    except IndexError:
        return ""


@login_required
def users(request, username="", feeds_form=None):
    if username:

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        feedss = Feeds.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):

            return render(request, 'user.html', {'user': user, 'feedss': feedss, })
        return render(request, 'user.html', {'user': user, 'feedss': feedss, 'follow': True, })
    users = User.objects.all().annotate(feeds_count=Count('feeds'))
    feedss = map(get_latest, users)
    obj = zip(users, feedss)
    feeds_form = feeds_form or FeedsForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'users':users,
                   'feeds_form': feeds_form,
                   'username': request.user.username,
                   'fname': request.user.first_name})


@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return render(request,'profiles.html')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
    return render(request,
                  'edit.html',
                  {'user_form': user_form,

                   'profile_form': profile_form})