
from django.urls import path
from . import views

urlpatterns=[
path('',views.login_view,name="login"),
path('signup/',views.signup_view,name="signup"),
path('dashboard/',views.dashboard,name="dashboard"),
path('add/',views.add_expense,name="add"),
path('delete/<int:id>/',views.delete_expense,name="delete"),
path('download/',views.download_csv,name="download"),
path('logout/',views.logout_view,name="logout"),
]
