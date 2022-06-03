# Generated by Django 4.0.4 on 2022-06-03 03:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
        ('stores', '0001_initial'),
        ('variations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordervariationsmodel',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='variations.variationmodel'),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='stores.storemodel'),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='variations',
            field=models.ManyToManyField(related_name='+', through='orders.OrderVariationsModel', to='variations.variationmodel'),
        ),
    ]