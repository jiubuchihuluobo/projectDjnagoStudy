from django.contrib.auth.views import LogoutView
from django.urls import path

from customauth.views import MyLoginView, MyRegisterView

app_name = "customauth"

urlpatterns = [
    # path("login/", HomeView.as_view(), name="login"),
    # path("logout/", LogOutView.as_view(), name="logout"),
    # path("register/", RegisterView.as_view(), name="register"),
    path("todo/login/", MyLoginView.as_view(), name="mylogin"),
    path('todo/logout/', LogoutView.as_view(next_page='customauth:mylogin'), name='mylogout'),
    path('todo/register/', MyRegisterView.as_view(), name='myregister'),
]
