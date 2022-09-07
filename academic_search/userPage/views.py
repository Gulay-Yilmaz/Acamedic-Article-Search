from django.shortcuts import render
from .forms import authorForm
# Create your views here.
import userPage.databaseQuery as dbQuery

def home_view(request):
    table = []
    form = authorForm(request.POST or None) 
    # print(table)
    context = {
            'formRadio': form,
            'table': table,
        }

    if form.is_valid():
        if request.POST['queryField'] == "authorName":
            appAuthorName = dbQuery.App()
            rows= appAuthorName.find_Author(request.POST['queryValue'],"name")
            rows2 = appAuthorName.find_author_publications(request.POST['queryValue'],"name")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"name":"Ad","surname":"Soyad","name2":"O. Çalışılan Ad","surname2":"O. Çalışılan Soyad"}
            column2 = {"name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            
            
            contextNew = {
            'formRadio': form2,
            'table': rows,
            'column': column,
            'column2': column2,
            'table2':rows2,
            'field':"name",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)

        if request.POST['queryField'] == "authorSurname":
            appAuthorName = dbQuery.App()
            rows= appAuthorName.find_Author(request.POST['queryValue'],"surname")
            rows2 = appAuthorName.find_author_publications(request.POST['queryValue'],"surname")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"ID":"ID","name":"Ad","surname":"Soyad","name2":"O. Çalışılan Ad","surname2":"O. Çalışılan Soyad"}
            column2 = {"ID":"ID","name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            contextNew = {
            'formRadio': form2,
            'table': rows,
            'column': column,
            'column2': column2,
            'table2':rows2,
            'field':"surname",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)

        if request.POST['queryField'] == "publicationName":
            appAuthorName = dbQuery.App()
            rows = appAuthorName.find_publications(request.POST['queryValue'],"name")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"ID":"ID","name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            contextNew = {
            'formRadio': form2,
            'column2': column,
            'table2':rows,
            'field':"Pname",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)

        if request.POST['queryField'] == "publicationDate":
            appAuthorName = dbQuery.App()
            rows = appAuthorName.find_publications(request.POST['queryValue'],"year")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"ID":"ID","name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            contextNew = {
            'formRadio': form2,
            'column2': column,
            'table2':rows,
            'field':"year",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)

        if request.POST['queryField'] == "publicationPlace":
            appAuthorName = dbQuery.App()
            rows = appAuthorName.find_types(request.POST['queryValue'],"place")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"ID":"ID","name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            contextNew = {
            'formRadio': form2,
            'column2': column,
            'table2':rows,
            'field':"place",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)

        if request.POST['queryField'] == "publicationType":
            appAuthorName = dbQuery.App()
            rows = appAuthorName.find_types(request.POST['queryValue'],"type")
            appAuthorName.close()
            form2 = authorForm(request.POST or None) 
            column = {"ID":"ID","name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
            contextNew = {
            'formRadio': form2,
            'column2': column,
            'table2':rows,
            'field':"type",
            'value':request.POST['queryValue'],
            }
            print("a",rows)
            return render(request, 'UserHome.html',contextNew)
        
    return render(request, 'UserHome.html',context)


def coauthor_view(request,name,surname):

    appAuthorName = dbQuery.App()
    rows= appAuthorName.find_Author(name,"name")
    rows2 = appAuthorName.find_author_publications(name,"name")
    appAuthorName.close()
    form2 = authorForm(request.POST or None) 
    column = {"name":"Ad","surname":"Soyad","name2":"O. Çalışılan Ad","surname2":"O. Çalışılan Soyad"}
    column2 = {"name":"Ad","surname":"Soyad","publicationName":" Yayın Adı","year":"Yayın Yılı","place":"Yayın Yeri","type":"Yayın Türü"}
    context = {
    'formRadio': form2,
    'table': rows,
    'column': column,
    'column2': column2,
    'table2':rows2,
    }
    print("a",rows)
    return render(request, 'CoauthorQuery.html',context)

def visualization_graph_view(request):
    return render(request, 'VisualizationGraph.html')

def query_view(request,field,value):
    context ={
        'query':""
    }
    if field == "name":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where a.name = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)
    if field == "surname":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where a.surname = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)
    if field == "Pname":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where b.name = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)
    if field == "year":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where b.year = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)
    if field == "place":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where c.year = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)
    if field == "type":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where c.type = "
        query2 ="return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization.html',context2)

    if field == "id":
        query1 = "Match(a:Author), (b:Publications), (c:Types), (a)-[r:ortak_calısır]-(d:Author) , (a)-[r2:yayın_yazarı]-(b), (b)-[r3:yayınlanır]-(c) where id(a) = "
        query2 =" return a,b,c,d,r,r2,r3"

        context2 = {
        'query1':query1,
        'query2':query2,
        'value':value,
        }
        return render(request, 'QueryVisualization2.html',context2)

    return render(request, 'QueryVisualization.html',context)

