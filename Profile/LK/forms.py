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
        fields = ['username', 'email', 'phone', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control sty1', 'placeholder':'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control sty1', 'placeholder':'Пароль'}))


class RegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control sty1', 'placeholder':'Логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control sty1', 'placeholder':'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Имя спортсмена'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Фамилия спортсмена'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Телефон'}))
    bd = forms.DateField(widget=MyDateInput(attrs={'class': 'form-control sty1', 'placeholder': 'Дата рождения спортсмена'}))
    city = forms.ModelChoiceField(queryset= City.objects.all(), widget=forms.Select(attrs={'class': 'form-control sty1', 'placeholder': 'Город'}))
    first_name_m = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control sty1', 'placeholder':'Имя родителя(необязательно)'}), required=False)
    last_name_m = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control sty1', 'placeholder':'Фамилия родителя(необязательно)'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'bd', 'city', 'first_name_m', 'last_name_m','password1', 'password2')


# class SportRegForm(forms.ModelForm):
#     class Meta:
#         model = Sportsman
#         fields = ['first_name_m', 'last_name_m', 'group', 'weight', 'passport']
#         widgets = {
#             'group': forms.Select(attrs={'class': 'form-control'}),
#             'filial': forms.HiddenInput(),
#             'club': forms.HiddenInput(),
#             'weight': forms.TextInput(attrs={'class': 'form-control'}),
#             'passport': forms.TextInput(attrs={'class': 'form-control'}),
#         }


class TrainerRegForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = '__all__'
    # username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control sty1', 'placeholder':'Логин'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control sty1', 'placeholder':'Email'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Имя '
    #                                                                                                         'спортсмена'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Фамилия '
    #                                                                                                        'спортсмена'}))
    # phone = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Телефон'}))
    # bd = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control sty1', 'placeholder': 'Дата рождения '
    #                                                                                                 'спортсмена'}))
    # city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control sty1', 'placeholder': 'Город'}))
    # club = forms.ModelChoiceField(queryset=Club.objects.all(), widget=forms.Select(attrs={'class': 'form-control sty1', 'placeholder': 'Клуб'}))
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Пароль'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1',
    #                                                               'placeholder': 'Подтвердите пароль'}))


    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'bd', 'city', 'club', 'password1',
    #               'password2')


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
        fields = ['title', 'content', 'club', 'city', 'photo', 'for_all']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'club': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'photo': forms.FileInput(),
            'for_all': forms.HiddenInput(),
        }


class UpdateSportsmen(forms.ModelForm):
    class Meta:
        model = User
        fields = ['city','club', 'filial', 'group', 'weight', 'passport', 'bio']
        widgets = {
            'city': forms.HiddenInput(),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club'].queryset = Club.objects.filter(city=self.initial['city'])
        self.fields['filial'].queryset = Filial.objects.filter(club=self.initial['club'])
        self.fields['group'].queryset = Group.objects.filter(filial=self.initial['filial'])


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'cost',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'filial': forms.HiddenInput(),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            # 'trainer': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['filial'].queryset = Filial.objects.filter(club=User.objects.get())


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
            'day': MyDateInput(attrs={'class':'form-select'}),
            'user': forms.HiddenInput(),

        }


class CreateStat(forms.ModelForm):

    class Meta:
        model = Statistic
        fields = ['day', 'status', 'user']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class':'form-control-input'}),
            'user': forms.HiddenInput(),
            'day': forms.HiddenInput()
        }


class ChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})