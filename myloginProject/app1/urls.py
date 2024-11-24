from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login"),
    path('home/', views.home_page, name="home"),
    path('logout/', views.Logout_user, name='Logout_user'),
    path('signup/', views.signup, name='signup'),

    #admin
    path('myadmin/',views.admin_login,name='myadmin'),
    path('adminhome/',views.admin_home,name='adminhome'),
    path('update/<id>',views.updateData,name='updateData'),
    path('delete/<id>',views.deleteData,name='deleteData'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('search',views.search,name='search'),

    path('new',views.demo,name="new")

]
