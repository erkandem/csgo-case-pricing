# Generated by Django 3.2.4 on 2021-07-10 21:39

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculationBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(blank=True, null=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.case')),
            ],
        ),
        migrations.CreateModel(
            name='CaseItemPriceApiResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('success', models.BooleanField()),
                ('status_code', models.IntegerField(blank=True, null=True)),
                ('average_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('median_price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('amount_sold', models.IntegerField(blank=True, null=True)),
                ('standard_deviation', models.FloatField(blank=True, null=True)),
                ('lowest_price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('highest_price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('first_sale_date', models.IntegerField(blank=True, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD')], max_length=10, null=True)),
                ('is_interpolated', models.BooleanField(default=False)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CsgoBackPackApiUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('api_url', models.URLField(blank=True, null=True)),
                ('case_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.caseitem')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CasePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('case_price', models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True)),
                ('case_key_price', models.DecimalField(blank=True, decimal_places=3, default=Decimal('2.5'), max_digits=20, null=True)),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD')], max_length=10, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prices.calculationbatch')),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_price', to='cases.case')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CaseItemPriceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD')], max_length=10, null=True)),
                ('case_price_fragment', models.DecimalField(blank=True, decimal_places=20, max_digits=40, null=True)),
                ('api_result', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='prices.caseitempriceapiresult')),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prices.calculationbatch')),
                ('case_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.caseitem')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='caseitempriceapiresult',
            name='api_url',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prices.csgobackpackapiurl'),
        ),
        migrations.AddField(
            model_name='caseitempriceapiresult',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prices.calculationbatch'),
        ),
        migrations.AddField(
            model_name='caseitempriceapiresult',
            name='case_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.caseitem'),
        ),
        migrations.AddConstraint(
            model_name='calculationbatch',
            constraint=models.UniqueConstraint(fields=('uuid',), name='unique batch uuid'),
        ),
    ]
