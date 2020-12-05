from lib2to3.fixes.fix_input import context
from django.db.models import Sum
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Budget.forms import AddExpensForm
# Create your views here.
from django.contrib.auth.decorators import login_required
from Budget.forms import RegistrationForm,LoginForm,ReviewExpense
from Budget.models import Expenses
def register(request):
    form=RegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
            context["form"]=form
            return render(request, "Budget/registration.html", context)
    return render(request,"Budget/registration.html",context)

def signIn(request):
    form=LoginForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return render(request, "Budget/home.html")
            else:
                return render(request, "Budget/login.html", context)
    return render(request,"Budget/login.html",context)

def signOut(request):
    logout(request)
    return redirect("signin")


def basePage(request):
    return render(request,"Budget/base.html")

@login_required
def editProfile(request):
    user=User.objects.get(username=request.user)
    form=RegistrationForm(instance=user)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RegistrationForm(instance=user,data=request.POST)
        # print("hello")
        if form.is_valid():
            # print("okay")
            form.save()
            return redirect("home")
        else:
            # print("not okey")
            context["form"]=form
            return redirect("edit")
    return render(request,"Budget/editprofile.html",context)


def userHome(request):
    return render(request, "Budget/home.html")

@login_required
def addExpens(request):
    form =AddExpensForm(initial={"user":request.user})
    context={}
    context["form"]=form
    expenses=Expenses.objects.filter(user=request.user)
    context["expenses"]=expenses
    if request.method=="POST":
        form=AddExpensForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpens")
        else:
            context["form"]=form
    return render(request,"Budget/adexpens.html",context)

@login_required
def editExpense(request,pk):
    id=Expenses.objects.get(id=pk)
    form=AddExpensForm(instance=id)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=AddExpensForm(instance=id,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpens")
            # print("save")
        else:
            context["form"]=form
            # print("not save")
    return render(request,"Budget/editexpense.html",context)

@login_required
def deleteExpense(request,pk):
    try:
        Expenses.objects.get(id=pk).delete()
        form=AddExpensForm()
        context={}
        context["form"]=form
        return redirect("addexpens")
    # print("delete")
    except Exception as e:
        return redirect("addexpens")
@login_required
def review_expens(request):
    form=ReviewExpense(initial={"user":request.user})
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ReviewExpense(request.POST)
        if form.is_valid():
            frmdate=form.cleaned_data.get("from_date")
            todate=form.cleaned_data.get("to_date")
            expense=Expenses.objects.filter(date__gte=frmdate,date__lte=todate,user=request.user)
            expenses=Expenses.objects.filter(date__gte=frmdate, date__lte=todate, user=request.user).values("amount")
            expen=Expenses.objects.filter(date__gte=frmdate, date__lte=todate, user=request.user).aggregate(Sum('amount'))
            expe =Expenses.objects.filter(date__gte=frmdate, date__lte=todate, user=request.user).values("amount").annotate(Sum('amount'))

            print(expen)
            tot=0
            for e in expenses:
                tot+=e["amount"]
            context["total"] = expen
            context["tot"]=tot
            context["totals"] = expe
            context["expens"]=expense

            return render(request, "Budget/reviewrexpense.html", context)
        else:
            context["form"]=form
    return render(request,"Budget/reviewrexpense.html",context)
