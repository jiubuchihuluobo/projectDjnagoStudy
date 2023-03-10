from django.urls import path

from todoapp.views import HomeView, TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, MyProfile

app_name = "todoapp"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("list/", TaskList.as_view(), name="tasks"),
    path('list/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('list/create/', TaskCreate.as_view(), name='create'),
    path('list/update/<int:pk>/', TaskUpdate.as_view(), name='update'),
    path('list/delete/<int:pk>/', TaskDelete.as_view(), name='delete'),
    path('user/profile/', MyProfile.as_view(), name="profile")
]
