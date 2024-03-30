from django.shortcuts import get_object_or_404, render, redirect

from .forms import CategoryForm, CreateUserForm, LoginForm, CreateTaskForm, UpdateTaskForm, PriorityForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from .models import Category, Priority, Task

# - VIEWS

def home(request):
    return render(request, 'index.html')

# - Registration

def register (request):

    form = CreateUserForm()
    
    if request.method == 'POST':
    
        form = CreateUserForm(request.POST)
    
        if form.is_valid():
    
            form.save()

            return redirect("my-login")
        
    context = {'form':form}
    
    return render(request, 'register.html', context=context)

# - Login

def my_login(request):

    form = LoginForm
    
    if request.method == 'POST':
    
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}
    
    return render(request, 'my-login.html', context=context)

# - Dashboard page

@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'profile/dashboard.html')
from .models import Category

# - User profile

def user_profile(request):
    return render(request, 'profile/user-profile.html')

# - Add category
@login_required(login_url='my-login')
def add_category(request):
    form = CategoryForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Assign the current user to the category
            category.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'profile/add-category.html', {'form': form})
# - View categories
@login_required(login_url='my-login')
def view_categories(request):
    categories = Category.objects.filter(user=request.user)  # Filter categories by current user
    return render(request, 'profile/view-categories.html', {'categories': categories})


# - Create a task

@login_required(login_url='my-login')

def createTask(request):

    form = CreateTaskForm()
    categories = Category.objects.all()
    priorities = Priority.objects.all()
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # cascade წაშლის გამო, ტასკის წაშლას მოჰყვება იუზერიც წაშლაც. so we need to take action!
            task.user = request.user #task will be linked to an user. user that is currently logged in.
            task.save()
            return redirect('view-tasks') 
    context = {'form':form, 'categories': categories, 'priorities': priorities}

    return render(request, 'profile/create-task.html', context=context)

# - Read all the tasks

@login_required(login_url='my-login')
def viewTask(request): 
    current_user = request.user.id #reference to primary key. to its ID
    
    task = Task.objects.filter(user=current_user)
    
    context = {'task' : task}

    return render(request, 'profile/view-tasks.html', context=context) 

# - Update task page

@login_required(login_url='my-login')
def updateTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view-tasks')
    else:
        form = UpdateTaskForm(instance=task)
    
    categories = Category.objects.all() 
    priorities = Priority.objects.all() 

    context = {'form': form, 'task': task}  # Pass the task object to the context
    return render(request, 'profile/update-task.html', context=context)

# - Delete task page
@login_required(login_url='my-login')
def deleteTask(request, pk): 

    task = Task.objects.get(id=pk)

    if request.method == 'POST':

        task.delete()

        return redirect('view-tasks')

    return render(request, 'profile/delete-task.html') 

# - Set priority
@login_required(login_url='my-login')
def set_priority(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data['priority']
            return render(request, 'success.html', {'priority': priority})
    else:
        form = PriorityForm()
    return render(request, 'set_priority.html', {'form': form})


# - Logout
def user_logout(request):

    auth.logout(request)

    return redirect("")