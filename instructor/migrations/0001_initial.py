# Generated by Django 5.1.4 on 2025-01-12 12:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='instructorRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching_before', models.CharField(max_length=200, null=True)),
                ('experience', models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('expert', 'expert')], max_length=100, null=True)),
                ('terms_conditions', models.BooleanField(default=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='courseCreateFirstStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('time', models.CharField(max_length=100)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('uid', models.CharField(max_length=50, null=True)),
                ('publish_true', models.BooleanField(default=False, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.instructorregister')),
            ],
        ),
        migrations.CreateModel(
            name='intendedLearner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_requirement', models.CharField(max_length=1000, null=True)),
                ('student_learn_1', models.CharField(max_length=200, null=True)),
                ('student_learn_2', models.CharField(max_length=200, null=True)),
                ('student_learn_3', models.CharField(max_length=200, null=True)),
                ('student_learn_4', models.CharField(max_length=200, null=True)),
                ('who_this_course', models.CharField(max_length=1000, null=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
            ],
        ),
        migrations.CreateModel(
            name='landingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('course_subtitle', models.CharField(max_length=150, null=True)),
                ('course_description', models.TextField()),
                ('level', models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('expert', 'expert'), ('all', 'all')], max_length=50)),
                ('coure_image', models.FileField(upload_to='course_image/')),
                ('promotional_video', models.FileField(upload_to='promotional_video/')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_price', models.CharField(max_length=200)),
                ('discount_percent', models.CharField(max_length=200)),
                ('after_discount_price', models.CharField(max_length=200)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('duration', models.CharField(blank=True, max_length=100, null=True)),
                ('position', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='instructor.module')),
            ],
        ),
        migrations.CreateModel(
            name='welcomeCongratMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('welcomeMsg', models.CharField(max_length=1000)),
                ('congratMsg', models.CharField(max_length=1000)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
            ],
        ),
        migrations.CreateModel(
            name='publishCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_length', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('totalLecture', models.CharField(max_length=200, null=True)),
                ('admin_aprove', models.BooleanField(default=False, null=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.coursecreatefirststep')),
                ('intended_lerner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.intendedlearner')),
                ('landing_page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.landingpage')),
                ('pricing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.pricing')),
                ('msg', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instructor.welcomecongratmessages')),
            ],
        ),
    ]
