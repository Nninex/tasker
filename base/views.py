from django.shortcuts import get_object_or_404, render, redirect
from .forms import CategoryForm, CreateUserForm, LoginForm, CreateTaskForm, UpdateTaskForm, PriorityForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,  login
from django.contrib.auth.decorators import login_required
from .models import Category, Priority, Task, UserProfile
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from .forms import ProfileUpdateForm
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
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            if Category.objects.filter(name=category.name, user=request.user).exists():
                messages.error(request, "Category with this name already exists.")
            else:
                category.save()
                messages.success(request, 'Category added successfully')
                return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'profile/add-category.html', {'form': form})

# - View categories

@login_required(login_url='my-login')
def view_categories(request):
    categories = Category.objects.filter(user=request.user)  # Filter categories by current user
    form = CategoryForm()
    return render(request, 'profile/view-categories.html', {'categories': categories, 'form':form})

# - Delete category
@login_required(login_url='my-login')
def deleteCategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        Task.objects.filter(category=category).delete() 
        category.delete()
        return redirect('view-categories')
    return render(request, 'profile/delete-category.html', {'category': category})

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
    task = Task.objects.filter(user=current_user).select_related('category', 'priority')
    categories = Category.objects.all()
    priorities = Priority.objects.all()
    
    context = {
        'task': task,
        'categories': categories,  
        'priorities': priorities, 
    }

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
        form = UpdateTaskForm(instance=task, initial={'title': task.title, 'content': task.content})
    categories = Category.objects.all() 
    priorities = Priority.objects.all() 
    context = {'form': form, 'task': task, 'categories': categories, 'priorities': priorities,}  # Pass the task object to the context
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

# - Update profile

@login_required(login_url='my-login')
def profile_update(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'profile/update-profile.html', {'user_form': user_form, 'profile_form': profile_form})

# - Logout

def user_logout(request):
    auth.logout(request)
    return redirect("")