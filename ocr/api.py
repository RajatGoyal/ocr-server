from tastypie.models import ApiKey
from models import Details
from pytesseract import image_to_string
from PIL import Image
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)

class Task(ModelResource):
    """
    API resource to add tasks to owl processor
    """
    class Meta:
        resource_name = 'task'
        queryset = Details.objects.all()
        # authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        # authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/jira/(?P<url>.*)$" % (self._meta.resource_name), self.wrap_view('proxy_get'), name="get_jira"),
            url(r"^(?P<resource_name>%s)/add%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('run_ocr'), name="add_task"),
            url(r"^(?P<resource_name>%s)/([^/]+%s)?$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('home'), name="home")
            ]

    def run_ocr(self,request, **kwargs):
        self.method_check(request, allowed=['post'])
        try:
            language = request.POST.get('language','eng')
            instance = Details.objects.create(image=request.FILES.get('image'))
            instance.save()
            image_obj = Image.open(instance.image.path).convert('RGB')
            instance.result = image_to_string(image_obj, lang=language)
            instance.save()
            result = instance.result
            response = self.create_response(request, {'success':True, 'result': result})
        except Exception, e:
            response = self.create_response(request, {'success': False, 'errMsg': str(e)})

        return response

    @csrf_exempt
    def proxy_get(self, request, url, **kwargs):
        url = url + "?"+request.META['QUERY_STRING']
        headers={"Authorization": request.META.get('HTTP_AUTHORIZATION')}
        resp = requests.get(url, headers=headers, data=request.REQUEST)
        return HttpResponse(resp.content, mimetype='application/json')


    def home(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        return self.create_response(request, {'success':True, 'message': 'only add action allowed'})

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        serializer = Serializer(formats=['json', 'jsonp'])
        always_return_data = True
        filtering = {
            'username': 'exact',
            'id': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect user information',
                }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)

class CreateUserResource(ModelResource):

    class Meta:
        allowed_methods = ['post']
        object_class = User
        resource_name = 'register'
        queryset = User.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username', 'id']
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        print "in create user resource"
        username, password = bundle.data['username'], bundle.data['password']
        try:
            bundle.obj = User.objects.create_user(username, '', password)

            try:
                api_key = ApiKey.objects.get(user_id=bundle.obj.id)
                api_key.key = None
                api_key.save()

            except ApiKey.DoesNotExist:
                print "api key error"
                api_key = ApiKey.objects.create(user=bundle.obj)

        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle