### django-analyticsds

#### Introduction

demiansoft 에서 사용하는 장고앱 django_analyticsds

---
#### Requirements

Django >= 5.0.3

---
#### Install

```
>> pip install django-analyticsds
```

settings.py

```
INSTALLED_APPS = [  
    ...
    
    'django_analyticsds',
]
```

---
#### Composition

네이버와 구글 애널리틱스 통계자료 수집을 위한 연결 코드를 만들어주는 앱

html 파일 내에서 다음 코드를 삽입하여 사용한다.
```html
{% load django_analyticsds_tags %}
{% make_analytics %}
```

프로젝트내 \_data 폴더안에 analyticsds.py 를 생성하여 다음의 형식으로 작성한다.
```
context = {  
    'analytics': {  
        'google_id': "구글 애널리틱스 아이디",  
        'naver_id': "네이버 애널리틱스 아이디",  
        'ads_id': "구글 애즈 아이디",  
        'conversion_click': {  
            # cta 버튼 수에 맞춰서 추가 한다.  
            'cta1': "전환추적 이벤트스니펫코드에서..",  
            'cta2': "전환추적 이벤트스니펫코드에서..",  
            'calling': "전환추적 이벤트스니펫코드에서..",  
        },  
    },  
}
```

1. 네이버 애널리틱스  
    - https://analytics.naver.com/ 에서 아이디 발급후 naver_id 변수에 입력  
2. 구글 애널리틱스  
    - https://analytics.google.com/ 에서 계정 및 속성 생성후 google_id 변수에 입력  
3. 구글 애즈  
    - ads_id 및 conversion_click, conversion_pageload 변수는 전환추적에 이용한다.  
    - https://ads.google.com/ 에서 전환을 생성하여 태그를 생성하여 이벤트 스니펫 코드를 등록한다.  
    (목표 - 전환 - 요약 - 전환 아이템에서 태그 설정)  
  
- conversion_click 딕셔너리 형식 의미  
  추적을 원하는 버튼 링크를 \<a href> 형식이 아닌 \<a onclick> 형식으로 제작하여 onclick에  {{ key }}\_gtag_report_conversion(url) 형식으로 함수를 호출한다.  
- cta 및 calling section 수정(함수 이름 맞추기)이 필요하다. 
