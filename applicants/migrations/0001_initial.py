# Generated by Django 2.2.6 on 2019-12-08 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application_info', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=20, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users_department', to='application_info.Department', verbose_name="User's department")),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users_university', to='application_info.University', verbose_name="User's university")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
