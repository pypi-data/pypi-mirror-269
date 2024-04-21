### django-bocor-ds

#### Introduction 
demiansoft homepage templates

---
#### Requirements

Django >= 5.0.3
libsass>=0.23.0
django-analyticsds >= 0.3.1
django-calendards >= 0.4.0
django-modalds >= 0.1.0
django-utilsds >= 0.4.0

---
#### Install

settings.py  
```  
INSTALLED_APPS = [    
    ...  
	'django_analyticsds',  
	'django_utilsds',  
	'django_calendards',  
	'django_modalds',  
	  
	'django_bocor_ds',
]

...

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '_static/'),
]

MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  
X_FRAME_OPTIONS = 'SAMEORIGIN'  
  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  

```

in the shell
```
>> pip install django-bocor-ds
>> python manage.py makemigrations django_calendards django_modalds
>> python manage.py migrate
>> python manage.py createsuperuser
```


urls.py
```
from django.contrib import admin  
from django.urls import path, include  
from django.conf import settings  
from django.conf.urls.static import static  
  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', include('django_bocor_ds.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---
#### Composition

프로젝트 내의 \_data 폴더 안에 bocords.py 파일을 생성하고 다음과 같은 형식으로 작성한다.

```
context = {}

context.update(base)
context.update(seo)
context.update(header)
context.update(hero)
context.update(clients)
context.update(about)
context.update(services)
context.update(features)
context.update(portfolio)
context.update(team)
context.update(pricing)
context.update(faq)
context.update(contact)
context.update(footer)

```
프로젝트 내의 \_static/img 폴더 안에 이미지파일을 넣어준다.

---

