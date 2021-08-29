from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import *


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'phone_dop', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_dop': forms.TextInput(attrs={'class': 'form-control'}),
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
    first_name_m = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Имя родителя'}))
    last_name_m = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Фамилия родителя'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control sty1', 'placeholder': 'Телефон'}))
    bd = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control sty1', 'placeholder': 'Дата рождения спортсмена'}))
    city = forms.ModelChoiceField(queryset= City.objects.all(), widget=forms.Select(attrs={'class': 'form-control sty1', 'placeholder': 'Город'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control sty1', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'first_name_m', 'last_name_m', 'phone', 'bd', 'password1', 'password2')


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
        fields = ['club', 'filial', 'group', 'weight', 'passport', 'bio', 'job']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'filial': forms.HiddenInput(),
            'club': forms.HiddenInput(),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'job': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filial'].queryset = Filial.objects.filter(club=self.initial['club'])
        self.fields['group'].queryset = Group.objects.filter(filial=self.initial['filial'])


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'cost', 'filial', 'trainer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filial': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['filial'].queryset = Filial.objects.filter(club=self.user.club)