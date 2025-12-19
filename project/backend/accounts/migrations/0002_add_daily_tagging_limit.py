# Generated migration for daily tagging limit

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='daily_tagging_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of tagging requests used today'),
        ),
        migrations.AddField(
            model_name='user',
            name='daily_count_reset_at',
            field=models.DateTimeField(blank=True, help_text='UTC timestamp of last daily reset', null=True),
        ),
        migrations.RemoveField(
            model_name='user',
            name='weekly_quota',
        ),
        migrations.RemoveField(
            model_name='user',
            name='quota_reset_at',
        ),
    ]
