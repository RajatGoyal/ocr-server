__author__ = 'rajatgoyal'

from tastypie.authorization import DjangoAuthorization
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from models import Details
from pytesseract import image_to_string
from PIL import Image

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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('run_ocr'), name="add_task"),
            url(r"^(?P<resource_name>%s)/([^/]+%s)?$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('home'), name="home")
            ]


    def run_ocr(self,request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        try:
            language = request.POST.get('language','eng')
            instance = Details.objects.create(File=request.FILES.get('image'))
            import code;code.interact(local=locals())
            instance.result = image_to_string(Image.open('test-european.jpg'), lang=language)
            instance.save()
            response = self.create_response(request, {'success':True})
        except Exception, e:
            response = self.create_response(request, {'success': False, 'errMsg': str(e)})

        return response

    def home(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        return self.create_response(request, {'success':True, 'message': 'only add action allowed'})

