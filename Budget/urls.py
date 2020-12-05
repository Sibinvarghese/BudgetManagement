
from django.contrib import admin
from django.urls import path
from Budget.views import  register,signIn,signOut,editProfile,userHome,addExpens,editExpense,deleteExpense,review_expens,basePage
urlpatterns = [
    path("",basePage),
    path("register",register,name="register"),
    path("signin",signIn,name="signin"),
    path("signout",signOut,name="signout"),
    path("edit",editProfile,name="edit"),
    path("home",userHome,name="home"),
    path("addexpens",addExpens,name="addexpens"),
    path("editExpense/<int:pk>",editExpense,name="editExpense"),
    path("deleteExpense/<int:pk>",deleteExpense,name="deleteExpense"),
    path("review/",review_expens,name="review"),
]
