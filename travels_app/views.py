from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Travel
from itertools import chain


def index(request):
    request.session.flush() 
    return render(request, 'index.html')


def loginForm(request):
   return render(request, 'login.html')


def register(request):
    errors=User.objects.register_validator(request.POST)
    if len(errors)>0:
       for key, value in errors.items():
           messages.error(request, value)
       return redirect('/loginForm')

    name=request.POST['name']
    username=request.POST['userName']    

    password=request.POST['password']
    pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    if len(User.objects.all()) == 0:
       level=1

    usuario=User.objects.create(name=name, user_name=username, password=pw_hash)

    messages.success(request, 'Congrats!!...User resgitrated!!')

    request.session['usuarioId']=usuario.id 
    return redirect ('/travel')


def login(request):
    currentUser=User.objects.filter(user_name=request.POST['loginUser'])

    errors=User.objects.login_validator(request.POST, currentUser)
    if len(errors)>0:
       for key, value in errors.items():
           messages.error(request, value)
       return redirect('/loginForm')

    else:
       request.session['usuarioId']=currentUser[0].id

    return redirect('/travel')


def logout(request):
    request.session.flush()
    messages.info(request,'Logged Out')
    return redirect('/')

########

def travel(request):
    if 'usuarioId' in request.session:
        usuario=User.objects.get(id=request.session['usuarioId'])

        allPlanned=usuario.planned_travels.all().values_list('id', flat=True)
        allJoined=usuario.travels.all().values_list('id', flat=True)
        userTravelsIds=list(chain(allPlanned, allJoined))
        allUserTravels=Travel.objects.filter(id__in=userTravelsIds)

        allOtherTravels=Travel.objects.exclude(id__in=userTravelsIds)        

        context={
            'name':usuario.user_name,
            'allUserTravels':allUserTravels,
            'allOtherTravels':allOtherTravels
        }

        return render(request, 'travel.html', context)
    else:
        return redirect('/loginForm')


def showDestination(request, dest_id):
    if 'usuarioId' in request.session:
        usuario=User.objects.get(id=request.session['usuarioId'])
        destination=Travel.objects.get(id=dest_id)
        tripUsers=destination.users.all().exclude(id=usuario.id).exclude(id=destination.planned_by.id)
        print(tripUsers)

        context={
            'name':usuario.user_name,
            'dest':destination,
            'tripUsers':tripUsers            
        }

        return render(request, 'showDest.html', context)

    else:
        return redirect('/loginForm')


def showFormAdd(request):
    if 'usuarioId' in request.session:
        usuario=User.objects.get(id=request.session['usuarioId'])
        context={
            'name':usuario.user_name
        }
        return render(request, 'addForm.html', context)

    else:
        return redirect('/loginForm')


def addTrip(request):
    if 'usuarioId' in request.session:

        errors=Travel.objects.travel_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/travels/add')

        usuario=User.objects.get(id=request.session['usuarioId'])
        dest=request.POST['destination']
        descr=request.POST['description']
        start=request.POST['startDate']
        end=request.POST['endDate']

        newTravel=Travel.objects.create(destination=dest, 
                                description=descr, 
                                start=start, 
                                end=end,
                                planned_by=usuario)

        usuario.travels.add(newTravel) #agrego el viaje a los travels del usuario que lo creo

        messages.info(request, "Your Trip Has Been Added!")

        return redirect("/travel")

    else:
        return redirect('/loginForm')


def join(request, travel_id):
    if 'usuarioId' in request.session:
        usuario=User.objects.get(id=request.session['usuarioId'])
        travel=Travel.objects.get(id=travel_id)

        usuario.travels.add(travel)
        
        messages.info(request, f"{travel.destination} has been added to your Schedule!")

        return redirect("/travel")

    else:
        return redirect('/loginForm')


##### END #####
