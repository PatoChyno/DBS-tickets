from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tickets_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^buy', 'tickets.views.buy_ticket'),
    url(r'^update', 'tickets.views.update_prices'),
    url(r'^delete', 'tickets.views.render_delete_event'),
    url(r'^stats', 'tickets.views.render_stats'),
    url(r'^bought', 'tickets.views.buy_ticket'),
    url(r'^$', 'tickets.views.index'),
)
