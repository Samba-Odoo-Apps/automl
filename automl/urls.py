"""automl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from auto.views import upload_doc_view, build_view,\
predict_view, upload_predict_view,\
predict_doc_list_view, build_delete_view
from django.views.generic import CreateView, ListView, TemplateView
from django.conf.urls.static import static
from auto.models import Document
from django.conf import settings
urlpatterns = [
    path("",TemplateView.as_view(
        template_name="auto/home.html"
        )),
    path('admin/', admin.site.urls),
    path("upload_build/",upload_doc_view),
    re_path("upload_predict/",upload_predict_view),

    path("list_models/",ListView.as_view(model=Document,)),
    re_path("list_predictions/(?P<pk>[0-9]*)", predict_doc_list_view),

    re_path("build/(?P<pk>[0-9]+)/$",build_view),
    re_path("build_delete/(?P<pk>[0-9]+)/$",build_delete_view),
    re_path("predict/(?P<pk>[0-9a-z_]+)/$", predict_view),
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
