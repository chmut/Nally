from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

from .models import *


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Логин'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Пароль'}))


class RegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': ' Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control sty1', 'placeholder': ' Email'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  empty_label=" Выберите город",
                                  widget=forms.Select(attrs={'class': 'form-control sty1 form-select', 'placeholder': 'Город'}))
    club = forms.ModelChoiceField(queryset=Club.objects.all(),
                                  empty_label=" Выберите клуб",
                                  widget=forms.Select(attrs={'class': 'form-control sty1 form-select'}))
    sportsman = forms.ModelChoiceField(queryset=Sportsman.objects.all(),
                                       empty_label=" Выберите спортсмена",
                                       widget=forms.Select(attrs={'class': 'form-control sty1 form-select'}))
    first_name = forms.HiddenInput()
    mid_name = forms.HiddenInput()
    last_name = forms.HiddenInput()
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': ' Телефон'}))
    bd = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control sty1',
                                                   'placeholder': ' Дата рождения спортсмена'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': ' Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1',
                                                                  'placeholder': ' Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'mid_name', 'last_name', 'email', 'bd', 'city', 'club',
                  'sportsman', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club'].queryset = Club.objects.none()
        self.fields['sportsman'].queryset = Sportsman.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['club'].queryset = Club.objects.filter(city_id=city_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['club'].queryset = self.instance.city.club_set

        if 'club' in self.data:
            try:
                club_id = int(self.data.get('club'))
                self.fields['sportsman'].queryset = Sportsman.objects.filter(club_id=club_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sportsman'].queryset = self.instance.club.sportsman_set


class TrainerRegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': ' Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control sty1', 'placeholder': ' Email'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  empty_label=" Выберите город",
                                  widget=forms.Select(attrs={'class': 'form-control sty1 form-select', 'placeholder': 'Город'}))
    club = forms.ModelChoiceField(queryset=Club.objects.all(),
                                  empty_label=" Выберите клуб",
                                  widget=forms.Select(attrs={'class': 'form-control sty1 form-select'}))
    trainer = forms.ModelChoiceField(queryset=Trainers.objects.all(),
                                       empty_label=" Выберите свое имя",
                                       widget=forms.Select(attrs={'class': 'form-control sty1 form-select'}))
    first_name = forms.HiddenInput()
    mid_name = forms.HiddenInput()
    last_name = forms.HiddenInput()
    bd = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control sty1',
                                                   'placeholder': ' Дата рождения спортсмена'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': ' Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1',
                                                                  'placeholder': ' Подтвердите пароль'}))
    job = forms.HiddenInput()

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'mid_name', 'last_name', 'email', 'bd', 'city', 'club',
                  'trainer', 'password1', 'password2', 'job')
        widgets = {
            'job': forms.HiddenInput(),
            'first_name': forms.HiddenInput(),
            'last_name': forms.HiddenInput(),
            'mid_name': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['club'].queryset = Club.objects.none()
    #     self.fields['trainer'].queryset = Sportsman.objects.none()
    #
    #     if 'city' in self.data:
    #         try:
    #             city_id = int(self.data.get('city'))
    #             self.fields['club'].queryset = Club.objects.filter(city_id=city_id)
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['club'].queryset = self.instance.city.club_set
    #
    #     if 'club' in self.data:
    #         try:
    #             club_id = int(self.data.get('club'))
    #             self.fields['trainer'].queryset = Trainers.objects.filter(club_id=club_id)
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['trainer'].queryset = self.instance.club.trainer_set


class UserOrders(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['name', 'size', 'status', 'client', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'color': forms.RadioSelect(),
            'client': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }


class CreateNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'club', 'city', 'photo', 'for_all', 'filial', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'club': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'photo': forms.FileInput(),
            'for_all': forms.HiddenInput(),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.HiddenInput()
        }


class CreateSportsman(forms.ModelForm):
    class Meta:
        model = Sportsman
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mid_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),
            'first_name_m': forms.TextInput(attrs={'class': 'form-control'}),
            'mid_name_m': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_m': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name_f': forms.TextInput(attrs={'class': 'form-control'}),
            'mid_name_f': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_f': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_dop': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['filial'].queryset = Filial.objects.filter(club=self.initial['club'])
        self.fields['group'].queryset = Group.objects.none()

        if 'filial' in self.data:
            try:
                filial_id = int(self.data.get('filial'))
                self.fields['group'].queryset = Group.objects.filter(filial_id=filial_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['group'].queryset = self.instance.filial.group_set


class UpdateSportsmen(forms.ModelForm):
    class Meta:
        model = Sportsman
        fields = ['filial', 'group', 'weight', 'passport', 'bio']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['filial'].queryset = Filial.objects.filter(club=self.initial['club'])
        self.fields['group'].queryset = Group.objects.filter(filial=self.initial['filial'])


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'cost', 'filial', 'trainer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.HiddenInput(),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['filial'].queryset = Filial.objects.filter(club=User.objects.get())


class GroupFormPro(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'cost', 'filial', 'trainer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.HiddenInput(),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'cost', 'filial', 'trainer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.HiddenInput(),
            'trainer': forms.HiddenInput(),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CreateDate(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ['day', 'user']
        widgets = {
            'day': MyDateInput(attrs={'class': 'form-select'}),
            'user': forms.HiddenInput(),

        }


class CreateStat(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ['day', 'status', 'user']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-control-input'}),
            'user': forms.HiddenInput(),
            'day': forms.HiddenInput()
        }


class ChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})


class UpdateCert(forms.ModelForm):
    class Meta:
        model = Certificates
        fields = ['cert_numb', 'data', 'belt', 'status']
        widgets = {
            'cert_numb': forms.TextInput(attrs={'class': 'form-control'}),
            'data': MyDateInput(attrs={'class': 'form-control'}),
            'belt': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(),
        }


class CreateCert(forms.ModelForm):
    class Meta:
        model = Certificates
        fields = ['person', 'cert_numb', 'data', 'belt', 'status']
        widgets = {
            'person': forms.Select(attrs={'class': 'form-control'}),
            'cert_numb': forms.TextInput(attrs={'class': 'form-control'}),
            'data': MyDateInput(attrs={'class': 'form-control'}),
            'belt': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.fields['filial'].queryset = Filial.objects.filter(club=self.initial['club'])
    #     self.fields['person'].queryset = Sportsman.objects.filter(club=user.club)


class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['title', 'address', 'trainer', 'type_of_pay', 'payment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'type_of_pay': forms.Select(attrs={'class': 'form-control'}),
            'payment': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Trainers
        fields = ['last_name', 'first_name', 'mid_name', 'salary']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mid_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderAdmin(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['name', 'size', 'status', 'client', 'color']
        widgets = {
            'name': forms.HiddenInput(),
            'size': forms.HiddenInput(),
            'color': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-control-sm'}),
        }