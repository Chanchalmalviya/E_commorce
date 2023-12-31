# Generated by Django 5.0 on 2023-12-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('description', models.TextField()),
                ('brand', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('MOBILE', 'MOBILE'), ('LAPTOP', 'LAPTOP'), ('TOPWERE', 'TOPWERE'), ('BOTTOMWERE', 'BOTTOMWERE'), ('ELECTRONIC', 'ELECTRONIC')], max_length=100)),
                ('product_image', models.ImageField(upload_to='producting/')),
            ],
        ),
    ]
