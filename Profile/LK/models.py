from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    jobs = (
        ('Спортсмен', 'Спортсмен'),
        ('Персонал', 'Персонал'),
    )
    mid_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Отчество спортсмена')
    email = models.EmailField(unique=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Город')
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Клуб')
    bd = models.DateField(auto_now=False, auto_now_add=False, null=True, verbose_name='Дата рождения спортсмена')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', null=True, blank=True, verbose_name='Аватарка')
    job = models.CharField(max_length=50, choices=jobs, default=jobs[0][0], verbose_name='Должность')
    sportsman = models.OneToOneField('Sportsman', on_delete=models.SET_NULL, null=True, blank=True)
    trainer = models.OneToOneField('Trainers', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()


class Sportsman(models.Model):
    gen = (('Мужской', 'Мужской'),
           ('Женский', 'Женский'))
    first_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Имя спортсмена')
    mid_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Отчество спортсмена')
    last_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Фамилия спортсмена')
    sex = models.CharField(max_length=7, choices=gen, default=gen[0][0], verbose_name='Пол')
    group = models.ForeignKey('Group', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Группа')
    filial = models.ForeignKey('Filial', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Филиал')
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Клуб')
    phone = models.CharField(max_length=20, null=True, verbose_name='Телефон')
    phone_dop = models.IntegerField(null=True, blank=True, verbose_name='Дополнительный телефон')
    first_name_m = models.CharField(blank=True, null=True, max_length=50, verbose_name='Имя родителя 1')
    mid_name_m = models.CharField(blank=True, null=True, max_length=50, verbose_name='Отчество родителя 1')
    last_name_m = models.CharField(blank=True, null=True, max_length=50, verbose_name='Фамилия родителя 1')
    first_name_f = models.CharField(blank=True, null=True, max_length=50, verbose_name='Имя родителя 2')
    mid_name_f = models.CharField(blank=True, null=True, max_length=50, verbose_name='Отчество родителя 2')
    last_name_f = models.CharField(blank=True, null=True, max_length=50, verbose_name='Фамилия родителя 2')
    weight = models.IntegerField(blank=True, null=True, verbose_name='Вес спортсмена')
    passport = models.CharField(blank=True, null=True, verbose_name='Номер паспорта спортсмена', max_length=100)
    bio = models.TextField(null=True, blank=True, max_length=1000, verbose_name='Описание')

    class Meta:
        verbose_name = 'Спортсмен'
        verbose_name_plural = 'Спортсмены'

    def __str__(self):
        return self.last_name


class Filial(models.Model):
    types=(
        ('Час', 'Почасовая'),
        ('Мес', 'Ежемесячная')
    )
    title = models.CharField(max_length=150, db_index=True, verbose_name='Имя филиала')
    address = models.CharField(max_length=150, null=True, verbose_name='Адрес')
    trainer = models.ForeignKey('Trainers', on_delete=models.PROTECT, verbose_name='Тренер')
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True, verbose_name='Клуб')
    type_of_pay = models.CharField(max_length=3, choices=types, default=types[0][0], verbose_name='Вид аренды')
    payment = models.IntegerField(blank=True, null=True, verbose_name='Стоимость аренды')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.title


class Trainers(models.Model):
    jobs = (
        ('Ассистент', 'Ассистент'),
        ('Тренер', 'Тренер'),
        ('Администратор филиала', 'Администратор филиала'),
        ('Администратор клуба', 'Администратор клуба'),
        ('Руководитель региона', 'Руководитель региона'),
        ('Руководитель клуба', 'Руководитель клуба'),
        ('Руководитель федерации', 'Руководитель федерации'),
    )
    first_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Имя тренера')
    mid_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Отчество тренера')
    last_name = models.CharField(blank=True, null=True, max_length=50, verbose_name='Фамилия тренера')
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Клуб')
    salary = models.IntegerField(null=True, verbose_name='Зарплата')
    phone = models.CharField(max_length=20, null=True, verbose_name='Телефон')
    job = models.CharField(max_length=50, choices=jobs, default=jobs[0][0], verbose_name='Должность')

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return self.last_name


class Certificates(models.Model):
    belts = (
        ('10 гуп', '10 гуп'),
        ('9 гуп', '9 гуп'),
        ('8 гуп', '8 гуп'),
        ('7 гуп', '7 гуп'),
        ('6 гуп', '6 гуп'),
        ('5 гуп', '5 гуп'),
        ('4 гуп', '4 гуп'),
        ('3 гуп', '3 гуп'),
        ('2 гуп', '2 гуп'),
        ('1 гуп', '1 гуп'),
        ('1 дан', '1 дан'),
        ('2 дан', '2 дан'),
        ('3 дан', '3 дан'),
        ('4 дан', '4 дан'),
        ('5 дан', '5 дан'),
        ('6 дан', '6 дан'),
        ('7 дан', '7 дан'),
        ('8 дан', '8 дан'),
        ('9 дан', '9 дан'),
    )
    cert_numb = models.CharField(max_length=30, default='000000', verbose_name='Номер сертификата')
    person = models.ForeignKey('Sportsman', on_delete=models.PROTECT, blank=True, null=True,
                               verbose_name='Пользователь (спортсмен)')
    trainer = models.ForeignKey('Trainers', on_delete=models.PROTECT, blank=True, null=True,
                               verbose_name='Пользователь (тренер)')
    status = models.BooleanField(default=0, verbose_name='Статус')
    data = models.DateField(verbose_name='Дата выдачи')
    belt = models.CharField(max_length=10, choices=belts, default=belts[0][0], verbose_name='Пояс')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.cert_numb


class Timetable(models.Model):
    days = (
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Суб', 'Суббота'),
        ('Вскр', 'Воскресенье'),
    )
    name = models.CharField(max_length=60, verbose_name='Название')
    time_b = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Время начала')
    time_e = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Время окончания')
    group = models.ForeignKey('Group', on_delete=models.PROTECT, null=True, verbose_name='Группа')
    day = models.CharField(max_length=4, choices=days, default=days[0][0], verbose_name='День недели')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Группа')
    cost = models.IntegerField(default=4000, verbose_name='Стоимость')
    filial = models.ForeignKey('Filial', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Филиал')
    trainer = models.ForeignKey('Trainers', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Инструктор')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    city = models.ForeignKey('City', on_delete=models.PROTECT,  verbose_name='Город')
    sportsmen = models.IntegerField(null=True, verbose_name='Количество спортсменов')

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=80, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    club = models.ForeignKey('Club', blank=True, null=True, on_delete=models.PROTECT,  verbose_name='Клуб')
    filial = models.ForeignKey('Filial', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Филиал')
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Город')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    # Тип Даты с автоматическим указанием даты и времени
    updated_at = models.DateField(auto_now=True, verbose_name='Обновлено')
    # Тип Даты с автоматическим указанием обновления даты и времени
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    author = models.ForeignKey('Trainers', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Автор')
    for_all = models.BooleanField(default=False, verbose_name='Для всех')

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-id']

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(max_length=80, verbose_name='Город')
    region = models.CharField(max_length=80, verbose_name='Регион')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Orders(models.Model):
    status = (
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('В пути', 'В пути'),
        ('Доставлено', 'Доставлено'),
    )
    colors = (
        ('Белый', 'Белый'),
        ('Желтый', 'Желтый'),
        ('Зеленый', 'Зеленый'),
        ('Синий', 'Синий'),
        ('Красный', 'Красный'),
        ('Черный', 'Черный'),
    )
    sizes = (
        ('100', '100'),
        ('110', '110'),
        ('120', '120'),
        ('130', '130'),
        ('140', '140'),
        ('150', '150'),
        ('160', '160'),
        ('170', '170'),
        ('180', '180'),
        ('190', '190'),
        ('200', '200'),
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )
    name = models.CharField(max_length=20, blank=True, verbose_name='Название', null=True)
    size = models.CharField(max_length=30, choices=sizes, blank=True, verbose_name='Размер', null=True)
    status = models.CharField(max_length=20, choices=status, default='Ожидает оплаты', verbose_name='Статус заказа', blank=True)
    color = models.CharField(max_length=40, choices=colors, verbose_name='Цвет', blank=True, null=True)
    client = models.ForeignKey('User', blank=True, null=True,  on_delete=models.PROTECT, verbose_name='Клиент')
    data = models.DateField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name


class Statistic(models.Model):
    user = models.ForeignKey('Sportsman', null=True, verbose_name='Спортсмен', on_delete=models.PROTECT)
    #user = models.ForeignKey('User', null=True, verbose_name='Спортсмен', on_delete=models.PROTECT)
    day = models.DateField(verbose_name='Дата', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Посещение')

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        ordering = ['day']

    def __str__(self):
        return str(self.user)