from django.db import models
from ckeditor.fields import RichTextField


class Age(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Duration(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Health(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Immigration(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Target(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Study(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Classification(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class ServicePath(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Integration(models.Model):
    text = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.text


class Service(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(verbose_name='Julkinen', default=False)
    ptv_service_id = models.CharField(max_length=100, blank=True, default='', verbose_name='PTV Palvelun id')
    ptv_servicechannel_id = models.CharField(max_length=100, blank=True, default='', verbose_name='PTV Palvelukanavan id')
    search_result_priority = models.PositiveIntegerField(blank=True, default=9, verbose_name='Hakutulosprioriteetti')
    name = models.CharField(max_length=100, blank=True, default='', verbose_name='Palvelun nimi')
    organization = models.TextField(blank=True, default='', verbose_name='Järjestävä organisaatio')
#    organization = models.CharField(max_length=100, blank=True, default='', verbose_name='Järjestävä organisaatio')
    ingress = models.TextField(blank=True, null=True, verbose_name='Ingressi')
    description = RichTextField(blank=True, null=True, verbose_name='Kuvaus', default='')
    description2 = RichTextField(blank=True, null=True, verbose_name='Kuvaus 2', default='')
    description3 = RichTextField(blank=True, null=True, verbose_name='Kuvaus 3', default='')
    description4 = RichTextField(blank=True, null=True, verbose_name='Kuvaus 4', default='')
    provider = RichTextField(blank=True, null=True, verbose_name='Toimija')
    benefit_effect = models.TextField(blank=True, null=True, verbose_name='Vaikuttaako tukiin')
    constraint = models.TextField(blank=True, default='', verbose_name='Palvelun rajaukset')
#    constraint = models.CharField(max_length=200, blank=True, default='', verbose_name='Palvelun rajaukset')
    open_ended = models.BooleanField(verbose_name='Voimassa toistaiseksi', default=False)
    start = models.DateField(blank=True, null=True, verbose_name='Voimassaolon alku')
    end = models.DateField(blank=True, null=True, verbose_name='Voimassaolon loppu')
    address = models.TextField(blank=True, null=True, verbose_name='Katuosoite')
    address_extend = models.CharField(max_length=100, blank=True, default='', verbose_name='Osoitteen tarkennus')
    post_address = models.TextField(blank=True, null=True, verbose_name='Postiosoite')
    contact_person = models.CharField(max_length=100, blank=True, default='', verbose_name='Yhteyshenkilö')
    contact_person_phone = models.TextField(blank=True, null=True, verbose_name='Puhelinnumero')
    contact_email = models.TextField(blank=True, null=True, verbose_name='Sähköposti')
    www = RichTextField(blank=True, null=True, verbose_name='Verkkosivu', default='')
    facebook = models.CharField(max_length=255, blank=True, default='', verbose_name='Facebook')
    twitter = models.CharField(max_length=255, blank=True, default='', verbose_name='Twitter')
    service_path = models.ManyToManyField(ServicePath, related_name='service_paths',
                                          verbose_name='Palvelupolku', blank=True)
    target = models.ManyToManyField(Target, related_name='targets', verbose_name='Tavoite', blank=True)
    study = models.ManyToManyField(Study, related_name='studies', verbose_name='Opiskelu', blank=True)
    classification = models.ManyToManyField(Classification, related_name='classifications',
                                            verbose_name='Palvelun luokka', blank=True)
    immigration = models.ManyToManyField(Immigration, related_name='immigration',
                                         verbose_name='Maahanmuuttotausta', blank=True)
    age_group = models.ManyToManyField(Age, related_name='age_groups', verbose_name='Ikäryhmä', blank=True)
    unemployment_duration = models.ManyToManyField(Duration, related_name='unemployment_durations',
                                                   verbose_name='Työttömyyden kesto', blank=True)
    health = models.ManyToManyField(Health, related_name='healths', verbose_name='Terveydentila / työkyky', blank=True)
    integration = models.ManyToManyField(Integration, related_name='integration',
                                         verbose_name='Kotouttaminen', blank=True)
    notes = RichTextField(blank=True, null=True, verbose_name='Palveluntarjoajan viestilaatikko', default='')
    content_contact = models.CharField(max_length=100, blank=True, default='', verbose_name='Sisällön yhteyshenkilö')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # addr = getattr(self, 'www')
        # if addr and not addr.startswith('http'):
        #     setattr(self, 'www', 'http://' + addr)
        # addr = getattr(self, 'facebook')
        # if addr and not addr.startswith('http'):
        #     setattr(self, 'facebook', 'http://' + addr)
        super(Service, self).save(*args, **kwargs)
