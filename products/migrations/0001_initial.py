# Generated by Django 4.0.4 on 2022-06-03 03:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('cost_value', models.FloatField()),
                ('sale_value_retail', models.FloatField()),
                ('sale_value_wholesale', models.FloatField()),
                ('quantity_wholesale', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('category_id', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.PROTECT, related_name='category', to='categories.categorymodel')),
                ('store_id', models.ForeignKey(db_column='store_id', on_delete=django.db.models.deletion.PROTECT, related_name='store', to='stores.storemodel')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': ' products',
                'db_table': 'products',
                'abstract': False,
            },
        ),
    ]