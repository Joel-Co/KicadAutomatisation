# Generated by Django 4.2.2 on 2023-06-30 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_resultfile_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultfile',
            name='pdf_file',
            field=models.FileField(default=None, upload_to='uploads/'),
        ),
    ]
