# -*- coding: utf-8 -*-
import traceback
import csv
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from .managers import CountryManager, CityManager
from django.db.models.signals import pre_save, pre_delete


class Country(models.Model):
    name = models.CharField(u"Название", max_length=100, unique=True)

    class Meta:
        verbose_name = u"Страна"
        verbose_name_plural = u"Страны"

    objects = CountryManager()

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(u"Название", max_length=100, db_index=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна')

    def get_iata(self):
        # TODO
        return "ROM"

    objects = CityManager()

    class Meta:
        verbose_name = u"Город"
        verbose_name_plural = u"Города"
        unique_together = "name", "country"
        ordering = "country__name", "name"

    def __unicode__(self):
        return u"{0}, {1}".format(self.country, self.name)


class AirportIATA(models.Model):

    iata = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    name_ru = models.CharField(max_length=100, blank=True, db_index=True)
    name_en = models.CharField(max_length=100, blank=True, db_index=True)
    coordinates = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    parent_name_en = models.CharField(max_length=100, blank=True, db_index=True)

    class Meta:
        verbose_name = _(u'IATA')
        verbose_name_plural = _(u'IATA')

    def __unicode__(self):
        return "{0}, {1} ({2})".format(self.name_en, self.parent_name_en, self.iata)


class UploadIATA(models.Model):

    RESULT = Choices(
        (0, 'success', 'Success'),
        (1, 'process', 'In process'),
        (2, 'error', 'Error'))

    csv_file = models.FileField(upload_to='iata',
        help_text=u"Сохранение нового файла удалить все существующие записи IATA и импортирует новые из этого файла")
    result = models.PositiveSmallIntegerField(choices=RESULT,
        default=RESULT.process)
    error_details = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Файл csv IATA')
        verbose_name_plural = _(u'Файлы csv IATA')

    def __unicode__(self):
        return self.csv_file.path

    @staticmethod
    def process_uploaded_csv(sender, instance, *args, **kwargs):
        if not instance.pk:
            # process upload only for first time
            try:
                result = UploadIATA.RESULT.success
                err_details = ""
                AirportIATA.objects.all().delete()
                reader = csv.reader(instance.csv_file, delimiter=",")
                # skip header line
                reader.next()
                for row in reader:
                    row_data = {}
                    row_data['iata'] = row[0]
                    row_data['type'] = row[1]
                    row_data['name_ru'] = row[2].decode("utf8")
                    row_data['name_en'] = row[3]
                    row_data['coordinates'] = row[4]
                    row_data['timezone'] = row[5]
                    row_data['parent_name_en'] = row[6]
                    AirportIATA(**row_data).save()
                instance.result = result
                instance.error_details = err_details
            except Exception:
                instance.result = UploadIATA.RESULT.error
                instance.error_details = traceback.format_exc()

    @staticmethod
    def process_deleted_csv(sender, instance, *args, **kwargs):
        if instance.csv_file:
            instance.csv_file.delete(False)

pre_save.connect(UploadIATA.process_uploaded_csv, sender=UploadIATA)
pre_delete.connect(UploadIATA.process_deleted_csv, sender=UploadIATA)
