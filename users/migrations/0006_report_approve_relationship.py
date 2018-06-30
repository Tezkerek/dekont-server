# Generated by Django 2.0.5 on 2018-06-30 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('users', '0006_auto_20180630_1056'), ('users', '0007_auto_20180630_1148'), ('users', '0008_auto_20180630_1212')]

    dependencies = [
        ('users', '0005_auto_20180624_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='parent',
        ),
        migrations.AddField(
            model_name='reportrelationship',
            name='approver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportrelationship',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RenameModel(
            old_name='ReportRelationship',
            new_name='ApproveReportRelationship',
        ),
        migrations.AddField(
            model_name='user',
            name='reporters',
            field=models.ManyToManyField(related_name='approvers', through='users.ApproveReportRelationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approvereportrelationship',
            name='approver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvers_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approvereportrelationship',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporters_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
