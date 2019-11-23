# Generated by Django 2.2.6 on 2019-11-19 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0001_initial'),
        ('events', '0004_auto_20191119_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='applicants.Applicant'),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('event', 'user')},
        ),
    ]
