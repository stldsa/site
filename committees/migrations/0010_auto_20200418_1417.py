# Generated by Django 3.0.5 on 2020-04-18 19:17

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('committees', '0009_auto_20200413_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committee',
            name='description',
        ),
        migrations.RemoveField(
            model_name='committee',
            name='slug',
        ),
        migrations.CreateModel(
            name='CommitteePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.fields.RichTextField(blank=True)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='committees.Committee')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
