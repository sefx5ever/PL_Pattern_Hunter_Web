# Generated by Django 3.2.2 on 2021-08-10 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_alter_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbolhistorydata',
            name='volume',
            field=models.IntegerField(default=False),
        ),
    ]
