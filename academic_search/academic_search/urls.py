"""academic_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from adminPage.views import login_view, add_author, add_journal, add_type, add_coauthor, type_publication
from userPage.views import home_view,coauthor_view,visualization_graph_view,query_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', home_view, name="home"),
    path(r'author/<str:name>/<str:surname>/', coauthor_view, name="coauthor"),
    path(r'adminLogin/', login_view, name="adminLogin"),
    path(r'addAuthor/', add_author, name="addAuthor"),
    path(r'addCoauthor/', add_coauthor, name="addCoauthor"),
    path(r'addType/', add_type, name="addType"),
    path(r'addJournal/', add_journal, name="addJournal"),
    path(r'typePublication/', type_publication, name="typePublication"),
    path(r'graph/', visualization_graph_view, name="graphVisualization"),
    path(r'query/<str:field>/<str:value>/', query_view, name="queryVis"),

    
]
