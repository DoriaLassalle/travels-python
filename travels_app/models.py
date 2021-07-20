from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
 
    def register_validator(self, data): #data trae los parametros por POST desde el formulario
        errors={}

        #primero valido si el email ya existe enla base
        if len(User.objects.filter(user_name=data['userName'])) >0:
            errors['userDuplicate']="This User already exists. Try another"


        else:
            if len(data['name'])<3:
                errors['name']="Name should be at least 3 characteres"

            if len(data['userName'])<3:
                errors['userName']="User Name name should be at least 3 characters"

                       
                        
            if data['password'] != data['confirmPw']:
                errors['pwMatch']="Passwords don't match"

            if len(data['password']) <8:
                errors['pwLength']="Password should be at least 8 characters"   

        return errors

    def login_validator(self, data, user):
        errors={}

        #si el usuario existe, validara la contraseña ingresada con la de la base
        if len(user)>0:

            if bcrypt.checkpw(data["loginPw"].encode(), user[0].password.encode()) is False:
                errors['loginPw']="Invalid User Data"
        
        else:
            errors['user']="Invalid User Data"
        
        return errors


class TravelManager(models.Manager):

    def travel_validator(self, data): 
        errors={}

        if len(data['startDate'])==0 or len(data['startDate']) <8 : #valido que la fecha traiga datos
                errors['startDateValid']="Date is invalid"
        if len(data['endDate'])==0 or len(data['endDate']) <8 : 
                errors['endDateValid']="Date is invalid"


        #si la fecha es correcta, la uso para las otras validaciones
        else:               
            now=datetime.now() #obtengo la fecha actual        
            start=datetime.strptime(data['startDate'], '%Y-%m-%d') #recibo la fecha ingresada que viene como str y la paso a formato de fecha  
            end=datetime.strptime(data['endDate'], '%Y-%m-%d')  

            if start < now:   #comparo fecha de inicio viaje que sea futura
                errors['start']="Date should be in the future." 

            if end < start: #comparo fecha término que sea despues de la de inicio
                errors['end']="Date should not be before 'From' date." 
           
        return errors



class User(models.Model):
    name=models.CharField(max_length=45)
    user_name=models.CharField(max_length=45)    
    password=models.CharField(max_length=255)   
    created_at=models.DateTimeField(auto_now_add=True)   
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    #planned_travels
    #travels

    def __repr__(self):
        return f"User: {self.name} {self.user_name}"

class Travel(models.Model):
    destination=models.CharField(max_length=45)
    description=models.TextField()
    start=models.DateField()
    end=models.DateField()
    planned_by=models.ForeignKey(User, related_name="planned_travels", on_delete=models.CASCADE)
    users=models.ManyToManyField(User, related_name="travels")
    created_at=models.DateTimeField(auto_now_add=True)   
    updated_at=models.DateTimeField(auto_now=True)
    objects=TravelManager()

    def __repr__(self):
        return f"User: {self.destination}"