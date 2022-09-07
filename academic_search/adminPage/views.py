from email import message
from multiprocessing import context
from django import views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import sqlite3
from django.urls import reverse
from datetime import datetime
import adminPage.databaseCreate as dbCreate


login_count = int(3)

db = sqlite3.connect('db.sqlite3', check_same_thread=False)
# db = sqlite3.connect("db.sqlite3")
file =db.cursor()

def login_view(request):

    # if request.user.is_authenticated:
    #     return redirect("home/")

    if request.method == "POST" :

        username = request.POST["username"]
        password = request.POST["password"]
        
        if username == "admin" and password == "admin":
            return render(request, "AdminHome.html")
    return render(request, "UserLogin.html")


    
def add_author(request):
    context={
        "message": ""
    }

    if request.method == "POST" :

        authorName = request.POST["authorName"]
        authorSurname = request.POST["authorSurname"]
        appAuthor= dbCreate.App()
        message = appAuthor.create_author(authorName,authorSurname)

        context2={
            "message": message

        }
        
        return render(request, "AddAuthor.html",context2)
        
    return render(request, "AddAuthor.html",context)

def add_journal(request):
    context={
        "message": ""
    }

    if request.method == "POST" :
        returnMessage = ""
     
        authorName = request.POST["authorName"]
        authorSurname = request.POST["authorSurname"]
        journalName = request.POST["journalName"]
        journalDate = request.POST["journalDate"]
        journalPlace = request.POST["journalPlace"]
        journalType = request.POST["journalType"]
        appAuthor= dbCreate.App()
        count = appAuthor.find_publication(journalName)
        count2 = appAuthor.find_type(journalType,journalPlace)
        if count == "0":
            if count2 == "0":
                appAuthor.create_type(journalType,journalPlace)
            
            returnMessage = appAuthor.create_publication_new(authorName,authorSurname,journalName,journalDate,journalPlace,journalType)
            print(count2)


        else:
            if count2 == "0":
                appAuthor.create_type(journalType,journalPlace)
            
            returnMessage = appAuthor.create_publication(authorName,authorSurname,journalName,journalDate,journalPlace,journalType)
            


        context2={
        "message": returnMessage
        }


        return render(request, "AddJournal.html",context2)
        
    return render(request, "AddJournal.html",context)

def add_type(request):

    context={
        "message": ""
    }
    if request.method == "POST" :

        place = request.POST["place"]
        type= request.POST["type"]
        appAuthor= dbCreate.App()
        message = appAuthor.create_type(type,place)

        context2={
            "message": message
        }

        return render(request, "AddType.html",context2)
        
    return render(request, "AddType.html",context)

    
def add_coauthor(request):
    
    context={
        "message": ""
    }
    if request.method == "POST" :

        authorName = request.POST["authorName"]
        authorSurname = request.POST["authorSurname"]
        coauthorName = request.POST["coauthorName"]
        coauthorSurname = request.POST["coauthorSurname"]
        appAuthor= dbCreate.App()
        message = appAuthor.create_coauthor_relationship(authorName, authorSurname, coauthorName, coauthorSurname)

        context2={
            "message": message
        }
        
        return render(request, "AddCoauthor.html",context2)
        
    return render(request, "AddCoauthor.html",context)

def type_publication(request):

    context={
        "message": ""
    }
    if request.method == "POST" :
        name = request.POST["name"]
        place = request.POST["place"]
        type= request.POST["type"]
        appAuthor= dbCreate.App()
        message = appAuthor.create_type_relationship(name,place,type)

        context2={
            "message": message
        }

        return render(request, "TypePublication.html",context2)
        
    return render(request, "TypePublication.html",context)
