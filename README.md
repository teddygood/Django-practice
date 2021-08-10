# Django-practice

Django로 블로그를 만들어보고 Docker로 배포합니다.

## Development envirionments

- Python version 3.7.6
- Django version 3.2.3
- Docker
- Docker-compose
- Gunicorn
- Nginx
- PostgreSQL

## Docker

### Development

1. 빌드 & 실행
   
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. `127.0.0.1:8000` 접속

3. 종료

```bash
docker-comppose -f docker-compose.dev.yml down -v
```

### Production

1. 빌드 & 실행

```bash
docker-compose -f docker-compose.yml up --build
```

2. `127.0.0.1` 접속

3. 종료

```bash
docker-compose -f docker-compose.yml down -v
```

### Migrate & createsuperuser

settings.py에 SECRET_KEY를 임의로 적용하고 migrate -> 이렇게 하지 않으면 `ImproperlyConfigured: The SECRET_KEY setting must not be empty` 에러가 뜰 수 있음. 도커에서 migrate 할 때는 SECRET_KEY를 지움 -> 어짜피 env 파일에 적용되어 있기 때문.

```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
docker-compose exec web python manage.py migrate
```

```bash
docker-compose exec web python manage.py createsuperuser
```

## Reference

### Book

[이성용, 김태곤, Do it! 장고+부트스트랩 파이썬 웹 개발의 정석, 이지스퍼블리싱, 2021](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9791163032069&orderClick=LAG&Kc=)

### django-crispy-forms

[commit 3425d09](https://github.com/teddygood/Django-practice/commit/3425d090509a60dee4c497aacfa7c46e7ff27326)

- [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5)
- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- [django-crispy-forms-doc](http://django-crispy-forms.rtfd.org/)

### markdown

[commit 787c4d4](https://github.com/teddygood/Django-practice/commit/787c4d4bb7e4f11930103c6a5d49ca2c0c2f1c8f)

- [markdodwn](https://github.com/Python-Markdown/markdown)  
- [Custom template tags and filters](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/)  
- [점프 투 장고 마크다운 기능 적용하기](https://wikidocs.net/71795)  

### SECRET_KEY

[commit 3ac25a2](https://github.com/teddygood/Django-practice/commit/3ac25a28d474656ec27d5f53d84cb1aa8b8ad1fd)
- [Cryptographic signing](https://docs.djangoproject.com/en/3.2/topics/signing/)
- [SECRET_KEY 변경 및 분리하기](https://wayhome25.github.io/django/2017/07/11/django-settings-secret-key/)
- [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/)
