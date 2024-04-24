### django-calendards  
  
#### Introduction  
  
demiansoft 에서 사용하는 장고앱 모음 django-calendards  
  
---  
#### Requirements  
  
Django >= 5.0.3  
  
---  
#### Install  
  
```  
>> pip install django_calendards  
>> python manage.py makemigrations django_calendards  
>> python manage.py migrate 
>> python manage.py createsuperuser #관리자로 접근해서 달력생성위해 
```  
  
settings.py  
  
```  
INSTALLED_APPS = [    
    ...  
	'django_calendards',  
]  
```  
  
---  
#### Composition    
##### calendards  
달력 형식의 팝업창을 띄워주는 앱. 팝업창은 한개만 activation이 가능하기 때문에 관리자 창에서 popupds 앱 포함 1개만 activation 시켜줘야 한다.  
  
html 파일 내에서 다음 코드를 삽입하여 사용한다.  
```html  
{% load django_calendards_tags %}  {% show_calendar %}  
```  
  
admin 페이지에서 calendar, event 테이블에 달력과 날짜를 세팅하여 사용한다.  
