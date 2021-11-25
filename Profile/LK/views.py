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
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
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
#     template_name = 'staff_registration.html'


def load_clubs(request):
    city_id = request.GET.get('city')
    clubs = Club.objects.filter(city_id=city_id)
    club_id = request.GET.get('club')
    sportsmen = Sportsman.objects.filter(club_id=club_id)
    return render(request, 'club_dropdown_list_options.html', {'clubs': clubs, 'sportsmen':sportsmen})


class SignUpView(CreateView):
    form_class = RegForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'

    def form_valid(self, form):
        self.form = form.save(commit=False)
        self.form.first_name = self.form.sportsman.first_name
        self.form.mid_name = self.form.sportsman.mid_name
        self.form.last_name = self.form.sportsman.last_name
        self.form.save()
        return super().form_valid(form)


class SignUpStaff(CreateView):
    form_class = TrainerRegForm
    success_url = reverse_lazy('login')
    template_name = 'staff_registration.html'

    def form_valid(self, form):
        self.form = form.save(commit=False)
        self.form.first_name = self.form.trainer.first_name
        self.form.mid_name = self.form.trainer.mid_name
        self.form.last_name = self.form.trainer.last_name
        self.form.job = 'Персонал'
        self.form.save()
        return super().form_valid(form)


@login_required
def profile(request):
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    password_form = ChangePassword(request.user, request.POST)
    try:
        cert = Certificates.objects.get(person=request.user.sportsman, status=True)
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
    if request.user.job == 'Спортсмен':
        news = News.objects.filter(club=request.user.club) | News.objects.filter(for_all=True) | News.objects.filter(city=request.user.city) | News.objects.filter(author=request.user.sportsman.group.trainer) | News.objects.filter(filial=request.user.sportsman.filial)
    else:
        news = News.objects.filter(club=request.user.club) | News.objects.filter(for_all=True) | News.objects.filter(city=request.user.city) | News.objects.filter(author = request.user.trainer)
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
    if request.user.job == 'Спортсмен':
        ord = Orders.objects.filter(client_id=request.user)
        context = {
            'ord': ord,
            'title': 'Заказы',
        }
        return render(request, 'lk/orders.html', context)
    else:
        return redirect('/orders_admin')


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


class DeleteOrder(DeleteView):
    model = Orders
    template_name = 'lk/orders.html'
    success_url = reverse_lazy('orders')


@login_required
def stat(request):
    stat = Statistic.objects.filter(user=request.user.sportsman)
    context = {
        'stat': stat,
        'title': 'Посещаемость',
    }
    return render(request, 'lk/statistic.html', context)


@login_required
def create_news(request):
    if request.user.trainer.job == 'Тренер':
        if request.method == 'POST':
            data = request.POST.copy()
            data['author'] = request.user.trainer
            form = CreateNews(data, request.FILES)
            if form.is_valid():
                news = News.objects.create(**form.cleaned_data)
                return redirect(news)
            else:
                print(form.errors)
        else:
            form = CreateNews()
        return render(request, 'lk/create_news.html', {"form": form})
    elif request.user.trainer.job == 'Руководитель клуба':
        if request.method == 'POST':
            data = request.POST.copy()
            data['club'] = request.user.club
            data['author'] = request.user.trainerpy
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
    if request.user.trainer.job == 'Тренер':
        groups = Group.objects.filter(trainer=request.user.trainer)
        sportsmen = Sportsman.objects.filter(group__trainer__exact=request.user.trainer)
        return render(request, 'lk/sportsmen.html', {"sportsmen": sportsmen, "groups": groups})
    if request.user.trainer.job == 'Руководитель клуба':
        filials = Filial.objects.filter(club=request.user.club)
        sportsmen = Sportsman.objects.filter(club=request.user.club)
        return render(request, 'lk/sportsmen.html', {"sportsmen": sportsmen, "filials": filials})
    else:
        return redirect('/')


@login_required
def create_sportsman(request):
    if request.user.trainer.job != 'Ассистент':
        if request.method == 'POST':
            data = request.POST.copy()
            data['club'] = Club.objects.get(name=request.user.trainer.club)
            form = CreateSportsman(data, request.FILES)
            if form.is_valid():
                sportsman = Sportsman.objects.create(**form.cleaned_data)
                return redirect(sportsmen)
            else:
                print(form.errors)
        else:
            form = CreateSportsman(initial={'club': request.user.trainer.club})
        return render(request, 'lk/create_sportsman.html', {"form": form})
    else:
        return redirect('/')


def load_groups(request):
    filial_id = request.GET.get('filial')
    groups = Group.objects.filter(filial_id=filial_id)
    return render(request, 'lk/sportsman_dropdown_list_options.html', {'groups': groups})


class DeleteSportsman(DeleteView):
    model = Sportsman
    template_name = 'lk/sportsmen.html'
    success_url = reverse_lazy('sportsmen')


@login_required
def sportsmen_group(request, group_id):
    if request.user.trainer.job != 'Ассистент':
        groups = Group.objects.filter(trainer=request.user.trainer)
        group = Group.objects.get(pk=group_id)
        sportsmen = Sportsman.objects.filter(group_id=group_id)
        return render(request, 'lk/sportsmen_group.html', {"sportsmen": sportsmen, "groups": groups, "group":group})
    else:
        return redirect('/')


@login_required
def sportsmen_filial(request, filial_id):
    if request.user.trainer.job == 'Руководитель клуба':
        filials = Filial.objects.filter(club=request.user.trainer.club)
        filial = Filial.objects.get(pk=filial_id)
        sportsmen = Sportsman.objects.filter(filial_id=filial_id)
        return render(request, 'lk/sportsmen_filial.html', {"sportsmen": sportsmen, "filials": filials, "filial":filial})
    else:
        return redirect('/')


class SportsmenUpdate(LoginRequiredMixin, UpdateView):
    model = Sportsman
    form_class = UpdateSportsmen
    template_name = 'lk/sportsmen_update.html'
    success_url = reverse_lazy('sportsmen')


@login_required
def groups(request):
    if request.user.trainer.job == 'Тренер':
        groups = Group.objects.filter(trainer=request.user.trainer)
        filials = Filial.objects.filter(group__trainer=request.user.trainer).distinct()
        return render(request, 'lk/groups.html', {"groups": groups, "filials":filials})
    elif request.user.trainer.job == 'Руководитель клуба':
        groups = Group.objects.filter(filial__club__exact=request.user.trainer.club)
        filials = Filial.objects.filter(club=request.user.trainer.club)
        return render(request, 'lk/groups.html', {"groups": groups, "filials":filials})
    else:
        return redirect('/')


@login_required
def filials(request, filial_id):
    if request.user.trainer.job == 'Руководитель клуба':
        filial = Filial.objects.get(pk=filial_id)
        groups = Group.objects.filter(filial=filial)
        filials = Filial.objects.filter(club=request.user.club)
        return render(request, 'lk/filial.html', {"groups": groups, "filials":filials, "filial":filial})
    elif request.user.trainer.job == 'Тренер':
        filial = Filial.objects.get(pk=filial_id)
        groups = Group.objects.filter(filial=filial, trainer=request.user.trainer)
        filials = Filial.objects.filter(group__trainer=request.user.trainer).distinct()
        return render(request, 'lk/filial.html', {"groups": groups, "filials":filials, "filial":filial})
    else:
        return redirect('/')


# class CreateGroup(LoginRequiredMixin, CreateView):
#     form_class = GroupForm
#     template_name = 'lk/create_group.html'
#     success_url = reverse_lazy('groups')
#
#     def form_valid(self, form):
#         fields = form.save(commit=False)
#         fields.trainer = Trainers.objects.get(name=self.request.user)
#         # if self.request.user.job == 'Руководитель клуба':
#         #     fields.filial.id = filial_id
#         # else:
#         #     fields.filial = self.request.user.filial
#         fields.filial = self.request.user.filial
#         fields.save()
#         return super().form_valid(form)


def create_group(request, filial_id):
    trainer = Trainers.objects.filter(club=request.user.trainer.club)
    if request.method == 'POST':
        if request.user.trainer.job == 'Руководитель клуба':
            data = request.POST.copy()
            data['filial'] = Filial.objects.get(id=filial_id)
            form = GroupFormPro(data, request.FILES)
            if form.is_valid():
                group = Group.objects.create(**form.cleaned_data)
                return redirect('groups')
            else:
                print(form.errors)
        else:
            data = request.POST.copy()
            data['filial'] = Filial.objects.get(id=filial_id)
            form = GroupForm(data, request.FILES)
            if form.is_valid():
                group = Group.objects.create(**form.cleaned_data)
                return redirect('groups')
    if request.user.trainer.job == 'Руководитель клуба':
        form = GroupFormPro()
    else:
        form = GroupForm()
    return render(request, 'lk/create_group.html', {"form":form})


class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = UpdateGroup
    template_name = 'lk/group_update.html'
    success_url = reverse_lazy('groups')


@login_required
def create_statistic(request):
    if request.user.trainer.job != 'Ассистент':
        user = Sportsman.objects.filter(group__trainer__exact=request.user.trainer)
        groups = Group.objects.filter(trainer=request.user.trainer)
        enddate = datetime.today()
        startdate = enddate - timedelta(days=7)
        stat = Statistic.objects.filter(user__group__trainer__exact=request.user.trainer, day__range=[startdate, enddate]).order_by("day")
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

                formset = formset(request.POST, request.FILES, queryset=Statistic.objects.filter(
                    user__group__trainer__exact=request.user.trainer, day__range=[startdate,enddate]).order_by("day"))
                if formset.is_valid():
                    formset.save()
                else:
                    print(formset.errors)

        form_date = CreateDate()
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)
        formset = formset(queryset=Statistic.objects.filter(user__group__trainer__exact=request.user.trainer, day__range=[startdate,enddate]).order_by("day"))
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
    if request.user.trainer.job != 'Ассистент':
        user = Sportsman.objects.filter(group_id=group_id)
        groups = Group.objects.filter(trainer=request.user.trainer)
        enddate = datetime.today()
        startdate = enddate - timedelta(days=7)
        stat = Statistic.objects.filter(user__group__exact=group_id,
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
                                                                    day__range=[startdate, enddate]).order_by("day"))
                if formset.is_valid():
                    formset.save()
                else:
                    print(formset.errors)

        form_date = CreateDate()
        formset = modelformset_factory(Statistic, form=CreateStat, extra=0)
        formset = formset(
            queryset=Statistic.objects.filter(user__group__exact=group_id,
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


@login_required
def cert_active(request):
    if request.user.trainer.job == 'Тренер':
        cert = Certificates.objects.filter(person__group__trainer__exact=request.user.trainer, status=1)
        return render(request, 'lk/cert_active.html', {"cert": cert,})
    if request.user.trainer.job == 'Руководитель клуба':
        cert = Certificates.objects.filter(person__club__exact=request.user.club, status=1)
        return render(request, 'lk/cert_active.html', {"cert": cert,})
    else:
        return redirect('/')


@login_required
def cert_all(request):
    if request.user.trainer.job == 'Тренер':
        cert = Certificates.objects.filter(person__group__trainer__exact=request.user.trainer)
        return render(request, 'lk/cert_all.html', {"cert": cert,})
    if request.user.trainer.job == 'Руководитель клуба':
        cert = Certificates.objects.filter(person__club__exact=request.user.club)
        return render(request, 'lk/cert_all.html', {"cert": cert,})
    else:
        return redirect('/')


class CertUpdate(LoginRequiredMixin, UpdateView):
    model = Certificates
    form_class = UpdateCert
    template_name = 'lk/cert_update.html'
    success_url = reverse_lazy('cert_active')


class CertCreate(LoginRequiredMixin, CreateView):
    model = Certificates
    form_class = CreateCert
    template_name = 'lk/cert_create.html'
    success_url = reverse_lazy('cert_active')


class FilialCreate(LoginRequiredMixin, CreateView):
    form_class = FilialForm
    template_name = 'lk/create_group.html'
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.club = Club.objects.get(name=self.request.user.trainer.club)
        fields.save()
        return super().form_valid(form)


class FilialUpdate(LoginRequiredMixin, UpdateView):
    model = Filial
    form_class = FilialForm
    template_name = 'lk/create_group.html'
    success_url = reverse_lazy('groups')


class FilialDelete(LoginRequiredMixin, DeleteView):
    model = Filial
    template_name = 'lk/groups.html'
    success_url = reverse_lazy('sportsmen')


@login_required
def personal(request):
    if request.user.trainer.job == 'Руководитель клуба':
        trainers = Trainers.objects.filter(club=request.user.trainer.club)
        return render(request, 'lk/personal.html', {"trainers": trainers,})
    else:
        redirect('/')


def personal_trainers(request):
    if request.user.trainer.job == 'Руководитель клуба':
        trainers = Trainers.objects.filter(club=request.user.trainer.club, job='Тренер')
        return render(request, 'lk/personal.html', {"trainers": trainers,})
    else:
        redirect('/')


def personal_admins(request):
    if request.user.trainer.job == 'Руководитель клуба':
        trainers = Trainers.objects.filter(club=request.user.trainer.club, job='Администратор филиала')
        return render(request, 'lk/personal.html', {"trainers": trainers,})
    else:
        redirect('/')


def create_personal(request):
    pass


class PersonalUpdate(LoginRequiredMixin, UpdateView):
    model = Trainers
    form_class = FilialForm
    template_name = 'lk/create_group.html'
    success_url = reverse_lazy('groups')


@login_required
def orders_admin(request):
    if request.user.trainer.job == 'Тренер':
        orders = Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer)
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset,})
    if request.user.trainer.job == 'Руководитель клуба':
        orders = Orders.objects.filter(client__club__exact=request.user.club)
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(
                                  client__club__exact=request.user.club))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__club__exact=request.user.club))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset})
    else:
        return redirect('/')


@login_required
def orders_admin_pay(request):
    if request.user.trainer.job == 'Тренер':
        orders = Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer, status='Ожидает оплаты')
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(
                                  client__sportsman__group__trainer__exact=request.user.trainer, status='Ожидает оплаты'))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer, status='Ожидает оплаты'))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset, })
    elif request.user.trainer.job == 'Руководитель клуба':
        orders = Orders.objects.filter(client__club__exact=request.user.club, status='Ожидает оплаты')
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(
                                  client__club__exact=request.user.club, status='Ожидает оплаты'))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__club__exact=request.user.club, status='Ожидает оплаты'))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset})
    else:
        return redirect('/')


@login_required
def orders_admin_way(request):
    if request.user.trainer.job == 'Тренер':
        orders = Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer,
                                       status='В пути')
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(
                                  client__sportsman__group__trainer__exact=request.user.trainer,
                                  status='В пути'))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer,
                                           status='В пути'))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset, })
    elif request.user.trainer.job == 'Руководитель клуба':
        orders = Orders.objects.filter(client__club__exact=request.user.club, status='В пути')
        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        if request.method == 'POST':
            formset = formset(request.POST, request.FILES,
                              queryset=Orders.objects.filter(
                                  client__club__exact=request.user.club, status='В пути'))

            if formset.is_valid():
                formset.save()
            else:
                print(formset.errors)

        formset = modelformset_factory(Orders, form=OrderAdmin, extra=0)
        formset = formset(
            queryset=Orders.objects.filter(client__club__exact=request.user.club, status='В пути'))
        return render(request, 'lk/orders_admin.html', {"orders": orders, "formset": formset})
    else:
        return redirect('/')


@login_required
def orders_admin_del(request):
    if request.user.trainer.job == 'Тренер':
        orders = Orders.objects.filter(client__sportsman__group__trainer__exact=request.user.trainer,
                                       status='Доставлено')

        return render(request, 'lk/orders_admin_del.html', {"orders": orders})
    if request.user.trainer.job == 'Руководитель клуба':
        orders = Orders.objects.filter(client__club__exact=request.user.club, status='Доставлено')

        return render(request, 'lk/orders_admin_del.html', {"orders": orders, })
    else:
        return redirect('/')