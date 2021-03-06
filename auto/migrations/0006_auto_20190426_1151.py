# Generated by Django 2.2 on 2019-04-26 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0005_auto_20190419_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='doc',
        ),
        migrations.RemoveField(
            model_name='document',
            name='doc_type',
        ),
        migrations.CreateModel(
            name='PredictDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('data', models.FileField(upload_to='')),
                ('doc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auto.Document')),
            ],
        ),
    ]
