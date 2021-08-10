# Generated by Django 3.2.4 on 2021-08-05 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LK', '0002_auto_20210801_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='LK.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='news',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='https://shvsm-penza.ru/wp-content/uploads/2020/11/maxresdefault-1.jpg', null=True, upload_to='avatar/%Y/%m/%d/', verbose_name='Аватарка'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='filial',
            name='payment',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость аренды'),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
    ]