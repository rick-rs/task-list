"""to_do_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/lista_tarefas/')),
    path('login/', views.login_user),
    path('lista_tarefas/', views.lista_tarefas),
    path('lista_tarefas/export', views.export_tarefas),
    path('lista_tarefas/import', views.import_tarefas),
    path('lista_tarefas/tarefa/', views.tarefa),
    path('lista_tarefas/tarefa/submit', views.submit_tarefa),
    path('lista_tarefas/tarefa/delete/<int:id_tarefa>', views.delete_tarefa),
    path('lista_tarefas/search', views.search_tarefa, name='search'),
    path('sobre/', views.about_us),
    path('admin/', admin.site.urls),
    path('login/submit', views.submit_login), 
    path('logout/', views.logout_user),
    path('register/', views.register_user),
    path('register/submit', views.register_user),
]
