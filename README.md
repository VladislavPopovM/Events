# Events

## Как запустить на локальном компьютере?

#### Загрузите код 
##### Код тестировался на python 3.7.4, Windows 10, Docker version 20.10.7

#### Запустите Docker-compose 
Перейдите в папку database и там введите следующие команды:
```
docker-compose up -d
```
#### Далее создайте суперпользователя:

##### Узнайте id контейнера
```
docker ps
```

##### Войдите в контейнер
```
docker exec -it <id> bash
```
##### Далее создайте суперпользователя
```
python ./main/manage.py createsuperuser
```

#### Переходите по ссылке: http://127.0.0.1:8000/

#### P.S: Чтобы пользователь смог создавать события, нужно в админке изменить тип клиента на 'staff' и
#### Чтобы сервис работал корректно, нужно поставить почту в settings.py
