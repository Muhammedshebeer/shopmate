# Generated by Django 5.2 on 2025-05-25 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textapp', '0009_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_products', to='textapp.categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='DealCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_products', to='textapp.categories'),
        ),
    ]
