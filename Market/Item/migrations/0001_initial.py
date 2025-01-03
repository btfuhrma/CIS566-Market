# Generated by Django 5.1.2 on 2024-10-25 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('handmade', 'Handmade'), ('collectible', 'Collectible'), ('general_market', 'General Market')], max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='item_images/')),
                ('addedDate', models.DateTimeField(auto_now_add=True)),
                ('is_sold', models.BooleanField(default=False)),
            ],
        ),
    ]
