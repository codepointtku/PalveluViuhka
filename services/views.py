from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.list import ListView
from django.conf import settings
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import get_view_name as original_get_view_name
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

from elasticsearch import Elasticsearch
from django.conf import settings

from .models import *


def update_index():
    es_settings = getattr(settings, "ELASTICSEARCH", "")
    es = Elasticsearch([es_settings])
    published_ids = set()
    for service in Service.objects.all():
        if service.publish:
            ser = ServiceSerializer(service)
            es.update(index='employment', doc_type='employment_service', id=service.id,
                      body={'doc': ser.data, 'doc_as_upsert': True})
            published_ids.add(service.id)
        else:
            es.delete(index='employment', doc_type='employment_service', id=service.id, ignore=[400, 404])

    for doc in es.search(index="employment")['hits']['hits']:
        if not int(doc['_id']) in published_ids:
            print(doc['_id'])
            es.delete(index='employment', doc_type='employment_service', id=int(doc['_id']), ignore=[400, 404])

class ServiceSerializer(serializers.ModelSerializer):
    health = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    target = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    service_path = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    classification = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    age_group = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    immigration = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    unemployment_duration = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')
    integration = serializers.SlugRelatedField(many=True, read_only=True, slug_field='text')

    class Meta:
        model = Service
        fields = ('id', 'name', 'search_result_priority', 'ingress', 'description', 'description2',
                  'description3', 'description4', 'constraint', 'open_ended', 'start', 'end', 'address',
                  'address_extend', 'post_address', 'organization', 'contact_person', 'contact_person_phone',
                  'contact_email', 'www', 'facebook', 'twitter', 'service_path', 'target',
                  'study', 'classification', 'immigration', 'age_group', 'unemployment_duration', 'health',
                  'integration', 'provider', 'benefit_effect')

    def to_representation(self, instance):
        ret = super(ServiceSerializer, self).to_representation(instance)
        if 'hanke tai projekti' in ret['classification']:
            ret['classification'].remove('hanke tai projekti')
        if 'muut tukipalvelut' in ret['classification']:
            ret['classification'].remove('muut tukipalvelut')
        return ret


class ServiceSerializerAPI(ServiceSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'created', 'labour_hire', 'publish', 'search_result_priority', 'name', 'organization', 'ingress',
            'description', 'description2', 'description3', 'description4', 'provider', 'benefit_effect', 'constraint',
            'open_ended', 'start', 'end', 'address', 'address_extend', 'post_address', 'contact_person',
            'contact_person_phone', 'contact_email', 'www', 'facebook', 'twitter', 'service_path', 'target', 'study',
            'classification', 'immigration', 'age_group', 'unemployment_duration', 'health', 'integration', 'notes',
            'content_contact'
        )
        # fields = ('id', 'name', 'search_result_priority', 'ingress', 'description', 'constraint',
        #           'open_ended', 'start', 'end', 'address',
        #           'address_extend', 'post_address', 'organization',
        #           'www', 'facebook', 'twitter', 'service_path', 'target',
        #           'classification', 'immigration', 'age_group', 'unemployment_duration', 'health',
        #           'integration')


class ServiceViewSet(ModelViewSet):
    #    queryset = Service.objects.all()
    serializer_class = ServiceSerializerAPI

    def get_queryset(self):
        queryset = Service.objects.all()
        queryset = queryset.filter(publish=True)     
        return queryset


def get_search(request):
    return render(request, "search.html")

def get_search_labour_hire(request):
    return render(request, "search_labour_hire.html")


@login_required
def post_edit_thank_you(request):
    return render(request, "thank_you.html", {'contact_email': getattr(settings, "CONTACT_EMAIL", "")})


def contact(request):
    return render(request, "contact.html", {'contact_email': getattr(settings, "CONTACT_EMAIL", "")})


def feedback_form(request):
    if request.method == 'POST':
        msg = MIMEText('Viite: ' + request.POST['ref'] + '\n\n' + request.POST['feedback'])
        msg['Subject'] = 'Palaute Työllisyysviuhkasta'
        msg['From'] = 'viuhka@turku.fi'
        msg['To'] = 'viuhka@turku.fi,arvi.leino@turku.fi'
        s = smtplib.SMTP('smtp.turku.fi')
        s.send_message(msg)
        s.quit()
    return render(request, "feedback_form.html",
                  {'contact_email': getattr(settings, "CONTACT_EMAIL", ""), 'ref': request.GET['ref']})


def info(request):
    return render(request, "info.html", {'contact_email': getattr(settings, "CONTACT_EMAIL", "")})


@login_required
def provider_info(request):
    return render(request, "provider_info.html", {'contact_email': getattr(settings, "CONTACT_EMAIL", "")})


class ServiceDetail(DetailView):
    model = Service
    template_name = 'details.html'

    def get_tags():
        tags = Tag.objects.all()
        return tags


class ServiceList(ListView):
    model = Service
    template_name = 'list.html'

    def get_queryset(self):
        queryset = super(ServiceList, self).get_queryset().order_by('name')
        return queryset.filter(publish=True)


service_fields = ('id', 'name', 'ingress', 'description', 'description2', 'description3', 'description4',
                  'constraint', 'open_ended', 'start', 'end', 'address',
                  'address_extend', 'post_address', 'organization', 'contact_person', 'contact_person_phone',
                  'contact_email', 'www', 'facebook', 'twitter', 'service_path', 'target',
                  'study', 'classification', 'immigration', 'age_group', 'unemployment_duration', 'health',
                  'integration', 'provider', 'benefit_effect', 'notes', 'content_contact')


class ServiceForm(LoginRequiredMixin, CreateView):
    fields = service_fields
    model = Service
    template_name = 'form.html'
    success_url = "/post_edit_thank_you/"


class ServiceEditForm(LoginRequiredMixin, UpdateView):
    fields = service_fields
    model = Service
    template_name = 'form.html'
    success_url = "/post_edit_thank_you/"

    def get_object(self, *args, **kwargs):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])
        service.publish = False
        return service

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
#        link_target_to_blank = ['description', 'www', 'provider', 'notes']
        link_target_to_blank = []
        for field in link_target_to_blank:
            soup = BeautifulSoup(request.POST[field], 'html.parser')
            links = soup.find_all('a')
            for link in links:
                link['target'] = '_blank'
            request.POST[field] = soup.prettify()
        result = super(ServiceEditForm, self).post(request, **kwargs)
        update_index()
        msg = MIMEText('https://tyollistymistaedistavatpalvelut.turku.fi/admin/services/service/')
        msg['Subject'] = 'Työllisyysviuhkassa on uusi tai muokattu palvelu'
        msg['From'] = 'viuhka@turku.fi'
        msg['To'] = 'viuhka@turku.fi,arvi.leino@turku.fi'
        s = smtplib.SMTP('smtp.turku.fi')
        s.send_message(msg)
        s.quit()
        return result

def get_view_name(cls, suffix=None):
    if cls.__name__ == 'APIRootView':
        return 'Employment Services'
    return original_get_view_name(cls, suffix)

def page_not_found(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    print(exception)

    return response