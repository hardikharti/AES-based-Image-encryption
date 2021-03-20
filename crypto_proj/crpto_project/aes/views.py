from django.shortcuts import render


from django.http import HttpResponse



#to import the Image form from form.py and image model from models.py 


from .form import ImageForm
from .models import Image





# Create your views here.
""" def home(response):
    return HttpResponse('<h1>THIS IS HOME PAGE FOR AES  </h1>') """

#this was just to print this is home for aes now we have home.html template

def home(request): #note that we have written REQUEST and not responce in the home function 
    return render(request,'aes/home.html',{})

def about(request): #note that we have written REQUEST and not responce in the home function 
    return render(request,'aes/about.html',{})

def encrypted(request): #note that we have written REQUEST and not responce in the home function 
    return render(request,'aes/encrypted.html',{})


def upload(request):
    
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            return render(request,"aes/upload.html",{"obj":obj})  
    else:
        form=ImageForm()    
        img=Image.objects.all()
    return render(request,"aes/upload.html",{"img":img,"form":form})