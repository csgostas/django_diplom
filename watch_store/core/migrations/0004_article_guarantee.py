# Generated by Django 5.0.7 on 2024-08-04 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_article_price_alter_article_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='guarantee',
            field=models.IntegerField(max_length=10, null=True, verbose_name='Гарантия'),
        ),
    ]
