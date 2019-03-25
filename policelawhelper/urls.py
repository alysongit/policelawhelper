"""policelawhelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve


class BaseSetting(object):
    enable_themes = True # 打开主题功能
    use_bootswatch = True #True主题比较多，False只有两个


class GlobalSetting(object):
    site_title = '交警法智数据管理系统'# 系统名称
    site_footer = '2019 擎盾数据, Inc.'# 底部版权栏
    # menu_style = "accordion"# 将菜单栏收起来

# 注册，注意一个是BaseAdminView，一个是CommAdminView
import xadmin
from xadmin import views
xadmin.site.register(views.BaseAdminView, BaseSetting) #
xadmin.site.register(views.CommAdminView, GlobalSetting)


urlpatterns = [
    path(r'admin/', xadmin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 指定上传媒体位置(方式一)
    path('ckeditor/', include('ckeditor_uploader.urls')),  #添加ckeditor的url到项目中

    path(r'api/app/', include("users.urls")),
    path(r'api/app/', include("cms.urls")),
    path(r'api/app/', include("illegal_action.urls")),

    path(r'api/pc/', include("users.urls")),
    path(r'api/pc/', include("cms.urls")),
    path(r'api/pc/', include("illegal_action.urls")),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) ## (方式二)没有这一句无法显示上传的图片