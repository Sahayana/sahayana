# Generated by Django 3.2.5 on 2021-09-25 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210922_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=1100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'main categories',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='main_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.maincategory'),
        ),
    ]
