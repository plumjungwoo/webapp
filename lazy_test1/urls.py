from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.first_view, name='first_view'),
    url(r'^uimage/$', views.uimage, name='uimage'),  # 유이미지라는 주소를 넣으면 뷰닷유이미지라는 함수로 내용 전달할거야.
    url(r'^dface/$', views.dface, name='dface'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)  # 이미지파일 업로드 설정
