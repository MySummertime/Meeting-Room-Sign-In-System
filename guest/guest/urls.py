"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from signSystem import views as v1


# named regular expression: (?P<name>pattern)
# unnamed regular expression: (pattern)


# www.xxx.com/index/ -> function
# url -> a function in views.py

urlpatterns = [
    path('admin/', admin.site.urls),

    # signSystem
    path('', v1.index),
    path('index/', v1.index, name='index'),
    path('accounts/login/', v1.index),
    path('login/', v1.login, name='login'),
    path('event_manage/', v1.eventManage, name='eventManage'),
    path('guest_manage/', v1.guestManage, name='guestManage'),
    path('search_event_name/', v1.searchEventName, name='searchEventName'),
    path('search_guest_name/', v1.searchGuestName, name='searchGuestName'),
    re_path(r'^sign_index/(?P<eid>[0-9]+)/$', v1.signIndex, name='signIndex'),
    path('sign_index_action/<int:eid>/', v1.signIndexAction, name='signIndexAction'),
    path('logout/', v1.logout, name='logout'),

    # api
    path('api/', include('api.urls')),
]
