# Generated by Django 5.1.6 on 2025-03-05 10:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalActivity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('action', models.CharField(choices=[('added', 'Added'), ('updated', 'Updated'), ('removed', 'Removed'), ('used', 'Used'), ('restocked', 'Restocked')], max_length=20)),
                ('quantity', models.FloatField(help_text='Change in quantity (positive for additions, negative for removals)')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='inventory.chemicals')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chemical_activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chemical Activities',
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['-timestamp'], name='inventory_c_timesta_72a9ff_idx'), models.Index(fields=['action'], name='inventory_c_action_c91891_idx'), models.Index(fields=['chemical'], name='inventory_c_chemica_a95b2e_idx'), models.Index(fields=['user'], name='inventory_c_user_id_ea9a20_idx')],
            },
        ),
    ]
