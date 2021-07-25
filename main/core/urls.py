from django.urls import path
from .views import (HomePageView, SignupPageView, personal_area, add_event_s, add_event_d,
                    participate_s, participate_d,json_Participate_s, json_Participate_d)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('personal_area/', personal_area, name='personal_area'),
    path('add_event_s/', add_event_s, name='add_event_s'),
    path('add_event_d/', add_event_d, name='add_event_d'),
    path('participate_s/<int:_id>/', participate_s, name='participate_s'),
    path('participate_d/', participate_d, name='participate_d'),
    path('json_Participate_s/<int:_id>/', json_Participate_s, name='json_Participate_s'),
    path('json_Participate_d/<int:_id>/', json_Participate_d, name='json_Participate_d'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
