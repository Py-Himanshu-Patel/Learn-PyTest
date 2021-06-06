# Generated by Django 3.2.4 on 2021-06-06 08:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('symbol', models.CharField(default='$', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('payment_intent_id', models.CharField(default=None, max_length=100, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Payment.currency')),
            ],
        ),
    ]