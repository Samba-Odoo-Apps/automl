# Generated by Django 2.2 on 2019-04-19 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_auto_20190419_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='doc',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='auto.Document'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='doc_type',
            field=models.CharField(choices=[('b', 'b'), ('p', 'p')], default='b', max_length=5),
        ),
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]