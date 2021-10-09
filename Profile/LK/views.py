from datetime import datetime, timedelta

from django.contrib.auth import update_session_auth_hash
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.core.paginator import Paginator


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'


# class SignUpDop(CreateView):
#     form_class = SportRegForm
#     success_url = reverse_lazy('login')
#     template_name = 'dop_registration.html'


class SignUpView(CreateView):
    form_class = RegForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


class Profile(UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('settings')
    template_name = 'lk/settings.html'


@login_required
def profile(request):
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    password_form = ChangePassword(request.user, request.POST)
    try:
        cert = Certificates.objects.get(person=request.user, status=True)
    except Certificates.DoesNotExist:
        cert = 0
    if request.method == 'POST':
        if request.POST.get("form_type") == 'edit_form':
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        elif request.POST.get("form_type") == 'pass_form':
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
            else:
                print(password_form.errors)
    else:
        form = UpdateForm(instance=request.user)
        password_form = ChangePassword(request.user, request.POST)
    return render(request, 'lk/profile.html', {"form": form, "cert": cert, "password_form":password_form})


@login_required
def news(request):
    city = City.objects.get(name=request.user.city)
    try:
        club = Club.objects.get(name=request.user.club)
        news = News.objects.filter(club=club) | News.objects.filter(for_all=True) | News.objects.filter(
            city=city)
    except Club.DoesNotExist:
        news = News.objects.filter(for_all=True)
    context = {
        # 'news': page_objects,
        'news': news,
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
        'ord': ord,
        'title': 'Заказы',
    }
    return render(request, 'lk/orders.html', context)


@login_required
def create_order(request):
    error = ''
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
        'stat': stat,
        'title': 'Посещаемость',
    }
    return render(request, 'lk/statistic.html', context)


@login_required
def create_news(request):
    if request.user.job == 'Тренер':
        # filial = Filial.objects.filter(title=request.user.filial)
        # club = Club.objects.filter(name=filial[0].club)
        club = Club.objects.get(name=request.user.club)
        if request.method == 'POST':
            data = request.POST.copy()
            data['club'] = Club.objects.get(name=request.user.club)
            data['city'] = City.objects.get(name=club.city)
            form = CreateNews(data, request.FILES)
            if form.is_valid():
                news = News.objects.create(**form.cleaned_data)
                return redirect(news)
            else:
                print(form.errors)
        else:
            form = CreateNews()
        return render(request, 'lk/create_news.html', {"form": form})
    elif request.user.job == 'Руководитель клуба':
        club = Club.objects.get(name=request.user.club)
        if request.method == 'POST':
            data = request.POST.copy()
            data['club'] = Club.objects.get(name=request.user.club)
            data['city'] = City.objects.get(name=club.city)
            form = CreateNews(data, request.FILES)
            if form.is_valid():
                news = News.objects.create(**form.cleaned_data)
                return redirect(news)
            else:
                print(form.errors)
        else:
            form = CreateNews()
        return render(request, 'lk/create_news.html', {"form": form})

    else:
        return redirect('/news/')


@login_required
def sportsmen(request):
    if request.user.job == 'Тренер':
        groups = Group.objects.filter(filial=request.user.filial)
        sportsmen = User.objects.filter(city=request.user.city, club=None, job='Спортсмен')
        return render(request, 'lk/sportsmen.html', {"sportsmen": sportsmen, "groups": groups})
    if request.user.job == 'Руководитель клуба':
        filials =Filial.objects.filter(club=request.user.club)
        sportsmen = User.objects.filter(city=request.user.city, club=None, job='Спортсмен')
        return render(request, 'lk/sportsmen.html', {"sportsmen": sportsmen, "filials": filials})
    else:
        return redirect('/')


@login_required
def sportsmen_group(request, group_id):
    if request.user.job != 'Спортсмен' or request.user.job != 'Ассистент':
        groups = Group.objects.filter(filial=request.user.filial)
        group = Group.objects.get(pk=group_id)
        sportsmen = User.objects.filter(group_id=group_id, job='Спортсмен')
        return render(request, 'lk/sportsmen_group.html', {"sportsmen": sportsmen, "groups": groups, "group":group})
    else:
        return redirect('/')


@login_required
def sportsmen_filial(request, filial_id):
    if request.user.job == 'Руководитель клуба':
        filials = Filial.objects.filter(club=request.user.club)
        filial = Filial.objects.get(pk=filial_id)
        sportsmen = User.objects.filter(filial_id=filial_id, job='Спортсмен')
        return render(request, 'lk/sportsmen_filial.html', {"sportsmen": sportsmen, "filials": filials, "filial":filial})
    else:
        return redirect('/')


class SportsmenUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateSportsmen
    template_name = 'lk/sportsmen_update.html'
    success_url = reverse_lazy('sportsmen')


@login_required
def groups(request):
    if request.user.job == 'Тренер':
        groups = Group.objects.filter(filial=request.user.filial)
        return render(request, 'lk/groups.html', {"groups": groups})
    elif request.user.job == 'Руководитель клуба':
        groups = Group.objects.filter(filial__club__exact=request.user.club)
        filials = Filial.objects.filter(club=request.user.club)
        return render(request, 'lk/groups.html', {"groups": groups, "filials":filials})
    else:
        return redirect('/')


@login_required
def filials(request, filial_id):
    if request.user.job == 'Руководитель клуба':
        filial = Filial.objects.get(pk=filial_id)
        groups = Group.objects.filter(filial=filial)
        filials = Filial.objects.filter(club=request.user.club)
        return render(request, 'lk/filial.html', {"groups": groups, "filials":filials, "filial":filial})
    else:
        return redirect('/')


class CreateGroup(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    template_name = 'lk/create_group.html'
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.trainer = Trainers.objects.get(name=self.request.user)
        fields.filial = self.request.user.filial
        fields.save()
        return super().form_valid(form)


class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = UpdateGroup
    template_name = 'lk/group_update.html'
    success_url = reverse_lazy('groups')


@login_required
def create_statistic(request):
    if request.user.job != 'Спортсмен' or request.user.job != 'Ассистент':
        user = User.objects.filter(filial=request.user.filial, job='Спортсмен')
        groups = Group.objects.filter(filial=request.user.filial)
        enddate = datetime.today()
        startdate = enddate - timedelta(days=7)
        stat = Statistic.objects.filter(user__filial__exact=request.user.filial, user__job__exact='Спортсмен', day__range=[startdate, enddate]).order_by("day")
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)


        if request.method == 'POST':

            if request.POST.get("form_type") == 'date':

                for pers in user:
                    data = request.POST.copy()

                    data['user'] = pers
                    form_date = CreateDate(data, request.FILES)

                    if form_date.is_valid():
                        Statistic.objects.create(**form_date.cleaned_data)
                    else:
                        print(form_date.errors)
            elif request.POST.get("form_type") == 'create':

                formset = formset(request.POST, request.FILES, queryset=Statistic.objects.filter(user__filial__exact=request.user.filial, user__job__exact='Спортсмен', day__range=[startdate,enddate]).order_by("day"))
                if formset.is_valid():
                    formset.save()
                else:
                    print(formset.errors)

        form_date = CreateDate()
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)
        formset = formset(queryset=Statistic.objects.filter(user__filial__exact=request.user.filial, user__job__exact='Спортсмен', day__range=[startdate,enddate]).order_by("day"))
        context = {
            "stat": stat,
            "pers": user,
            "form": form_date,
            "form_create": formset,
            "groups": groups,
        }

        return render(request, 'lk/statistic_admin.html', context)
    else:
        return redirect('/')


def get_group_stat(request, group_id):
    if request.user.job != 'Спортсмен' or request.user.job != 'Ассистент':
        user = User.objects.filter(group_id=group_id, job='Спортсмен')
        groups = Group.objects.filter(filial=request.user.filial)
        enddate = datetime.today()
        startdate = enddate - timedelta(days=7)
        stat = Statistic.objects.filter(user__group__exact=group_id, user__job__exact='Спортсмен',
                                        day__range=[startdate, enddate]).order_by("day")
        group = Group.objects.get(pk=group_id)
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)

        if request.method == 'POST':

            if request.POST.get("form_type") == 'date':

                for pers in user:
                    data = request.POST.copy()

                    data['user'] = pers
                    form_date = CreateDate(data, request.FILES)

                    if form_date.is_valid():
                        Statistic.objects.create(**form_date.cleaned_data)
                    else:
                        print(form_date.errors)
            elif request.POST.get("form_type") == 'create':

                formset = formset(request.POST, request.FILES,
                                  queryset=Statistic.objects.filter(user__group__exact=group_id,
                                                                    user__job__exact='Спортсмен',
                                                                    day__range=[startdate, enddate]).order_by("day"))
                if formset.is_valid():
                    formset.save()
                else:
                    print(formset.errors)

        form_date = CreateDate()
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)
        formset = formset(
            queryset=Statistic.objects.filter(user__group__exact=group_id, user__job__exact='Спортсмен',
                                              day__range=[startdate, enddate]).order_by("day"))
        context = {
            "stat": stat,
            "pers": user,
            "form": form_date,
            "form_create": formset,
            "groups": groups,
            "group":group,
        }

        return render(request, 'lk/statistic_group.html', context)
    else:
        return redirect('/')
