from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from . models import Category, Task

# = Register an user
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

# - Login an user
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a task
    
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content']
        exclude = ['user',]
# - Update a task
        
class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'priority']
        exclude = ['user']

# - categories
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Category Name'}

    def clean_name(self):
        name = self.cleaned_data['name']
        return name
# - Priorities
class PriorityForm(forms.Form):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

