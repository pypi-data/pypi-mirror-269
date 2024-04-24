### django-modalds

#### Introduction

demiansoft 에서 사용하는 장고 홈페이지 템플릿 모음 django-modalds

---
#### Requirements

Django >= 5.0.3
pillow >= 10.2.0

---
#### Install

```
>> pip install django_modalds
>> python manage.py makemigrations django_modalds
>> python manage.py migrate
```

settings.py

```
INSTALLED_APPS = [  
    ...
    
    'django_modalds',
]

...

MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

---
#### Composition

이미지 형식의 팝업창을 띄워주는 앱 형식에 따라 5가지를 준비해 놓았다. 팝업창은 한개만 activation이 가능하기 때문에 관리자 창에서 django_calendards 앱 포함 1개만 activation 시켜줘야 한다.

html 파일 내에서 다음 코드를 삽입하여 사용한다.
```html
{% load django_modalds_tags %}  
{% show_modal %}
```

admin 페이지에서 type1 - 5 테이블에 형식을 세팅하여 사용한다.
