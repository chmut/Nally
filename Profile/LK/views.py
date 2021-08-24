from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UpdateForm, LoginUserForm, RegForm, UserOrders
from django.views import generic
from .models import *


class LoginUser (LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'


class SignUpView(generic.CreateView):
    form_class = RegForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


@login_required
def profile(request):
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    cert = Certificates.objects.filter(person=request.user) & Certificates.objects.filter(status=True)
    group = Group.objects.filter(name=request.user.group)
    if group.exists():
        filial = Filial.objects.filter(title=group[0].filial)
        club = Club.objects.filter(name=filial[0].club)
    else:
        filial = 'Не выбран'
        club = 'Не выбран'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    form = UpdateForm()

    return render(request, 'lk/profile.html', {"form": form, "cert": cert, "filial": filial})


@login_required
def news(request):
    group = Group.objects.filter(name=request.user.group)
    if group.exists():
        filial = Filial.objects.filter(title=group[0].filial)
        club = Club.objects.filter(name=filial[0].club)
        novosti = News.objects.filter(club=club[0].pk)|News.objects.filter(for_all=True)
    else:
        novosti =News.objects.filter(for_all=True)
    context = {
        'news': novosti,
        'title': 'Новости',
    }
    return render(request, template_name='lk/news.html', context=context)


@login_required
def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'lk/view_news.html', {"item": news_item})


@login_required
def orders(request):
    ord = Orders.objects.filter(client_id=request.user)
    context = {
        'ord':ord,
        'title': 'Заказы',
    }
    return render(request, 'lk/orders.html', context)


@login_required
def create_order(request):
    error=''
    form1 = UserOrders()
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form1 = UserOrders(request.POST)
            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.client = request.user
                form1.name = 'Добок'
                form1.color = 'Белый'
                form1.save()
            else:
                print(form1.errors)
        elif request.POST.get("form_type") == 'formTwo':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form2 = UserOrders(request.POST)
            if form2.is_valid():
                form2 = form2.save(commit=False)
                form2.client = request.user
                form2.name = 'Футы'
                form2.save()
            else:
                print(form2.errors)
        elif request.POST.get("form_type") == 'formThree':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form3 = UserOrders(request.POST)
            if form3.is_valid():
                form3 = form3.save(commit=False)
                form3.client = request.user
                form3.name = 'Перчатки'
                form3.save()
            else:
                print(form3.errors)
        elif request.POST.get("form_type") == 'formFour':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form4 = UserOrders(request.POST)
            if form4.is_valid():
                form4 = form4.save(commit=False)
                form4.client = request.user
                form4.name = 'Шлем'
                form4.save()
            else:
                print(form4.errors)
        elif request.POST.get("form_type") == 'formFive':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form5 = UserOrders(request.POST)
            if form5.is_valid():
                form5 = form5.save(commit=False)
                form5.client = request.user
                form5.size = '180'
                form5.name = 'Пояс'
                form5.save()
            else:
                print(form5.errors)
        elif request.POST.get("form_type") == 'formSix':
            data = request.POST.copy()
            data.update({'user': request.user.id})
            form6 = UserOrders(request.POST)
            if form6.is_valid():
                form6 = form6.save(commit=False)
                form6.client = request.user
                form6.color = 'Белый'
                form6.name = 'Книга'
                form6.save()
            else:
                print(form6.errors)
    form1 = UserOrders()
    form2 = UserOrders()
    form3 = UserOrders()
    form4 = UserOrders()
    form5 = UserOrders()
    form6 = UserOrders()
    data = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
        'form6': form6,
        'error': error,
    }
    return render(request, 'lk/create_order.html', data)


@login_required
def stat(request):
    stat = Statistic.objects.filter(user_id=request.user)
    context = {
        'stat':stat,
        'title': 'Посещаемость',
    }
    return render(request, 'lk/statistic.html', context)
