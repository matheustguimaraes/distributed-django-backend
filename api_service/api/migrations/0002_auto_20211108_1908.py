# Generated by Django 3.1.7 on 2021-11-08 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userrequesthistory',
            options={'ordering': ['-date'], 'verbose_name': 'User Request History', 'verbose_name_plural': 'User Requests'},
        ),
        migrations.AlterField(
            model_name='userrequesthistory',
            name='close',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userrequesthistory',
            name='high',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userrequesthistory',
            name='low',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='userrequesthistory',
            name='open',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
