from django.conf.urls import  url
from django.conf.urls.static import static
from django.contrib import admin

from pro import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^$', 'feeds.views.index'),
    url(r'^signup$', 'feeds.views.signup'),
    url(r'^login$', 'feeds.views.login_view'),
    url(r'^logout$', 'feeds.views.logout_view'),
    url(r'^feedss$', 'feeds.views.public'),
    url(r'^submit$', 'feeds.views.submit'),
    url(r'^users/$', 'feeds.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'feeds.views.users'),
    url(r'^follow$', 'feeds.views.follow'),
    url(r'^password-change/$','django.contrib.auth.views.password_change',name='password_change'),
    url(r'^password-change/done/$','django.contrib.auth.views.password_change_done',name='password_change_done'),
    url(r'^edit/$', 'feeds.views.edit', name='edit'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

