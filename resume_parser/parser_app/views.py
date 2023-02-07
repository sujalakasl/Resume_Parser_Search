from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
import os
from .forms import RegisterForm
from django.contrib.auth import logout

def homepage(request):
    if request.method == 'POST':
        #Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()
                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name               = data.get('name')
                    resume.email              = data.get('email')
                    resume.mobile_number      = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education      = ', '.join(data.get('degree'))
                    else:
                        resume.education      = None
                    resume.designation        = data.get('designation')
                    resume.total_experience   = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills         = ', '.join(data.get('skills'))
                    else:
                        resume.skills         = None
                    if data.get('experience') is not None:
                        resume.experience     = ', '.join(data.get('experience'))
                    else:
                        resume.experience     = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            context = {
               'resumes': resumes,
            }
            #return redirect('http://127.0.0.1:8000/homepage')
            return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})

       
        

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("http://127.0.0.1:8000/login/")
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form":form})

def table(request):
        homepage(request)
        resumes=Resume.objects.all()
        context = {
               'resumes': resumes,
            }
        return render(request, 'base.html', context)

def logout_view(request):
    logout(request)
    return render (request, 'login.html')

def search_db(request):
    if request.method == "POST":
        searched = request.POST['searched']
        skill=Resume.objects.filter(name__contains = searched) or Resume.objects.filter(skills__contains = searched) or Resume.objects.filter(email__contains = searched) or Resume.objects.filter(designation__contains = searched)
        return render(request, 'search-db.html',{'searched' : searched, 'skill': skill})
    else:
        return render(request, 'search-db.html',{})



    
     





