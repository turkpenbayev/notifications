# Generated by Django 3.1 on 2022-12-01 21:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='task_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
