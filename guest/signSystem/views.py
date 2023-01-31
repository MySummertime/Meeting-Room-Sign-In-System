
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models.event import Event
from .models.guest import Guest

# Create your views here.


def index(req):
    '''Home Page'''
    return render(req, 'index.html')


def login(req):
    '''Log in'''
    # get
    if req.method == 'GET':
        return render(req, 'index.html', locals())
    # post
    else:
        user = req.POST.get('user', '')
        pwd = req.POST.get('pwd', '')
        person = auth.authenticate(username=user, password=pwd) # authentication before login attempt
        if person is not None:
            auth.login(req, person) # login
            req.session['user'] = user  # store session in browser
            res = HttpResponseRedirect('/event_manage/')
            return res
        else:
            return render(req, 'index.html', {'err': 'User name or Password error!'})


@login_required
def eventManage(req):
    '''Events Management'''
    user = req.session.get('user', '')  # read session in browser
    lst = Event.objects.all()   # read all events from db

    # Set Paginator of 2 items
    pgt = Paginator(lst, 2)
    p = req.GET.get('page') # get the index of page that will be rendered
    try:
        # return the page of index p
        e = pgt.page(p)
    except PageNotAnInteger:
        # if index p is not exist, return the first page
        e = pgt.page(1)
    except EmptyPage:
        # if index p is out of bound, return the last page
        e = pgt.page(pgt.num_pages)

    return render(req, 'event_manage.html', {'user': user, 'events': e})


@login_required
def searchEventName(req):
    user = req.session.get('user', '')
    search_name = req.GET.get('name', '')
    #print(user, search_name)
    lst = Event.objects.filter(name__icontains=search_name) # ignore letter case
    print(lst)
    return render(req, 'event_manage.html', {'user': user, 'events': lst})


@login_required
def signIndex(req, eid):
    '''Sign page after guest click sign in event_manage.html'''

    e = get_object_or_404(Event, id=eid)    # if object does not exist, throw a Http404 exception
    print(e)
    return render(req, 'sign_index.html', {'event': e})


@login_required
def signIndexAction(req, eid):
    '''Sign Action when guest click sign in sign_index.html'''

    # if object does not exist, return a Http404 page
    e = get_object_or_404(Event, id=eid)    # if object does not exist, return a Http404 page

    phone = req.POST.get('phone', '')
    print(phone)

    # authenticate phone number
    res = Guest.objects.filter(phone=phone)
    if not res:
        return render(req, 'sign_index.html', {'event': e, 'hint': 'Wrong Phone Number.'})

    # authenticate phone number && event id
    res = Guest.objects.filter(phone=phone, event_id=eid)
    if not res:
        return render(req, 'sign_index.html', {'event': e, 'hint': 'Wrong Event ID or Phone Number.'})

    # authenticate whether the guest has signed
    res = Guest.objects.get(phone=phone, event_id=eid)
    if res.sign:
        return render(req, 'sign_index.html', {'event': e, 'hint': 'User has signed.'})

    # sign the guest in
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(req, 'sign_index.html', {'event': e, 'hint': 'User signed successfully', 'guest': res})


'''Guests Management
'''
@login_required
def guestManage(req):
    user = req.session.get('user', '')  # read session in browser
    lst = Guest.objects.all()   # read all events from db

    # Set Paginator of 2 items
    pgt = Paginator(lst, 2)
    p = req.GET.get('page') # get the index of page that will be rendered
    try:
        # return the page of index p
        g = pgt.page(p)
    except PageNotAnInteger:
        # if index p is not exist, return the first page
        g = pgt.page(1)
    except EmptyPage:
        # if index is out of bound, return the last page
        g = pgt.page(pgt.num_pages)

    return render(req, 'guest_manage.html', {'user': user, 'guests': g})


@login_required
def searchGuestName(req):
    user = req.session.get('user', '')
    search_name = req.GET.get('name', '')
    #print(user, search_name)
    lst = Guest.objects.filter(realname__icontains=search_name) # ignore letter case
    #print(lst)
    return render(req, 'guest_manage.html', {'user': user, 'guests': lst})


@login_required
def logout(req):
    '''Log out'''
    auth.logout(req)    # log out
    res = HttpResponseRedirect('/index/')
    return res