# Generated by Django 2.1.3 on 2019-01-07 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('axfday', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_selected', models.BooleanField(default=True)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axfday.Goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '购物车',
            },
        ),
        migrations.CreateModel(
            name='MineBtns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btn', models.CharField(max_length=30)),
                ('class_name', models.CharField(max_length=100)),
                ('bref_url', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': '我的页面的下一排按钮',
            },
        ),
        migrations.AlterIndexTogether(
            name='cart',
            index_together={('user', 'goods')},
        ),
    ]
