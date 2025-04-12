# Generated by Django 5.1.4 on 2025-03-07 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_chemicalactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemicalactivity',
            name='action',
            field=models.CharField(choices=[('added', 'Added'), ('updated', 'Updated'), ('removed', 'Removed'), ('used', 'Used'), ('restocked', 'Restocked'), ('report_generated', 'Report Generated')], max_length=20),
        ),
    ]
