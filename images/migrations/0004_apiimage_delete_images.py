# Generated by Django 4.1.7 on 2023-02-28 11:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import images.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0003_images_delete_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=512, upload_to=images.models.user_directory_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('expires_after', models.IntegerField(default=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
