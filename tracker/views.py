
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Expense
from django.http import HttpResponse
import csv

def predict_category(text):
    keywords={
        "Food":["pizza","burger","restaurant"],
        "Travel":["uber","bus","train","taxi"],
        "Shopping":["amazon","flipkart","mall"],
        "Bills":["electricity","water","internet"]
    }
    text=text.lower()
    for category,words in keywords.items():
        for w in words:
            if w in text:
                return category
    return "Other"

def signup_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        User.objects.create_user(username=username,password=password)
        return redirect("login")
    return render(request,"signup.html")

def login_view(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect("dashboard")
    return render(request,"login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    expenses=Expense.objects.filter(user=request.user)
    total=sum(e.amount for e in expenses)
    return render(request,"dashboard.html",{"expenses":expenses,"total":total})

def add_expense(request):
    if request.method=="POST":
        desc=request.POST['description']
        amount=request.POST['amount']
        date=request.POST['date']
        category=predict_category(desc)

        Expense.objects.create(
            user=request.user,
            description=desc,
            amount=amount,
            category=category,
            date=date
        )
        return redirect("dashboard")
    return render(request,"add_expense.html")

def delete_expense(request,id):
    expense=Expense.objects.get(id=id)
    expense.delete()
    return redirect("dashboard")

def download_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="expenses.csv"'
    writer=csv.writer(response)
    writer.writerow(['Description','Amount','Category','Date'])
    expenses=Expense.objects.filter(user=request.user)
    for e in expenses:
        writer.writerow([e.description,e.amount,e.category,e.date])
    return response
