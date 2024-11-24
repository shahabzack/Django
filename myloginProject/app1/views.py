from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.cache import never_cache
import re


from django.db.models import Q


#admin
from .models import Student
from .forms import StudentInsertForm


@never_cache
def login_page(request):
    if 'name' in request.session:
        return redirect(home_page)

    if request.method == 'POST':
        username = request.POST.get('name', '')
        pass1 = request.POST.get('password', '')

        try:
            student = Student.objects.get(name=username, password=pass1)
            request.session['name'] = username
            return redirect(home_page)
        except Student.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')


@never_cache
def home_page(request):
     if 'name' in request.session:
        
        return render(request, 'home.html')
     return redirect(login_page)


def Logout_user(request):
        if 'name' in request.session:
            request.session.flush()
        return redirect(login_page)


def is_valid_username(username):

    return bool(re.match("^[a-zA-Z][a-zA-Z0-9]*$", username))


def signup(request):
    if 'name' in request.session:
        return redirect(home_page)

    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not is_valid_username(username):
            messages.error(request, 'Username must start with letters')
            return redirect('signup')

        if Student.objects.filter(name=username).exists():
            messages.error(request, 'Username is already taken. Please choose another one.')
            return redirect('signup')

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please use another email.')
            return redirect('signup')

        if password == confirm_password:
            student = Student(name=username, email=email, password=password)
            student.save()
            return redirect('login')
        else:
            messages.error(request, 'Password & Confirm Password Must Be the Same')
            return redirect('signup')

    return render(request, 'signup.html')


#admin
@never_cache
def admin_login(request):
    if 'username' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')

        user = authenticate(username=username, password=pass1)
        if user is not None:
            request.session['username'] = username
            return redirect(admin_home)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('myadmin')
    
    return render(request, 'adminlogin.html')

@never_cache
def admin_home(request):
    if 'username' in request.session:
        if request.method == 'POST':
            form = StudentInsertForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                if Student.objects.filter(name=name).exists() or Student.objects.filter(email=email).exists():
                    messages.error(request, 'Username or Email already exists. Please use a different one.')
                else:
                    query = Student(name=name, email=email, password=password)
                    query.save()
                    messages.success(request, 'Data Inserted Successfully')
                    return redirect('adminhome')
            else:
                messages.error(request, 'Error inserting data. Please check the form.')
        else:
            form = StudentInsertForm()

        data = Student.objects.all()
        context = {"form": form, "data": data}
        return render(request, 'adminhome.html', context)

    
    request.session.clear()
    return redirect(admin_login)

@never_cache
def updateData(request, id):
    if 'username' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']

            existing_name = Student.objects.exclude(id=id).filter(name=name).exists()
            existing_email = Student.objects.exclude(id=id).filter(email=email).exists()

            if existing_name or existing_email:
                messages.error(request, 'Username or Email already exists. Please use a different one.')
            else:
                edit = get_object_or_404(Student, id=id)
                edit.name = name
                edit.email = email
                edit.save()
                messages.success(request, 'Data Updated Successfully')

            return redirect('adminhome')

        d = get_object_or_404(Student, id=id)
        context = {"d": d}

        return render(request, 'edit.html', context)
@never_cache
def deleteData(request, id):
    d = get_object_or_404(Student, id=id)
    d.delete()
    messages.error(request, "Data Deleted Successfully")
    return redirect('adminhome')

@never_cache
def adminlogout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect(admin_login)


def search(request):
    query = request.GET.get('query', '')
    allPosts = Student.objects.all()
    params = {'allPosts': allPosts}
    return render(request, 'search.html', params)

def search(request):
    query = request.GET.get('query', '')
    allPosts = Student.objects.filter(name__icontains=query) | Student.objects.filter(email__icontains=query)   # Using case-insensitive partial match

    # Debug information
    debug_info = {
        'query': query,
        'num_results': allPosts.count(),
    }

    params = {
        'allPosts': allPosts,
        'debug_info': debug_info,
    }
    return render(request, 'search.html', params)


def demo(request):
    context = {
        'name':[{"name":"fass",
                 "place":"kannur"
                 },
                 {"name":"fast",
                 "place":"kzd"
                 }
                 ]
    }
    return render(request,'rev.html',context)