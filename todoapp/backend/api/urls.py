from django.urls import path
from .import views

urlpatterns = [
    path('todos/', views.ToDoListCreate.as_view(), name='list'),
    path('todos/<int:pk>', views.ToDoRetrievUpdateDestroy.as_view(), name='destroy'),
    path('todos/<int:pk>/complete', views.ToDoToggleComplete.as_view(), name='complete'),
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.Login, name='login'),
]
