import profile
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [

    #--------HomePage--------#
    path('', views.home, name = ""),

    #----Register an user----#
    path('register', views.register, name='register'),
    
    #------Login an user-----#
    path('my-login', views.my_login, name='my-login'),
     
    #-----Dashboard page-----#
    path('dashboard', views.dashboard, name='dashboard'),

    #-----Create a task------#
    path('create-task', views.createTask, name="create-task"),
    
    #-----Read the tasks-----#
    path('view-tasks', views.viewTask, name="view-tasks"),
    
    #-----Update a task------#
    path('update-task/<str:pk>/', views.updateTask, name="update-task"), #dynamic 
    
    #-----Delete a task------#
    path('delete-task/<str:pk>/', views.deleteTask, name="delete-task"),
    
    #-----Logout an user-----#
    path('user-logout', views.user_logout, name="user-logout"),
   
    #------Add category------#
    path('add-category/', views.add_category, name='add-category'),

    #----View categories-----#
    path('view-categories/', views.view_categories, name='view-categories'),
    
    #----Delete category-----#
    path('delete-category/<int:category_id>/', views.deleteCategory, name='delete-category'),
    
    #-----User profile ------#
    path('profile/', views.user_profile, name='profile'),

    #-----Update profile ------#
    path('profile-update/', views.profile_update, name='profile-update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)