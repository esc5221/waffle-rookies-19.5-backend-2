# 와플스튜디오 Backend Seminar[4] 과제

## esc5221 / 최병욱
_________________________________________

## **1번** 
![Image](https://github.com/esc5221/waffle-rookies-19.5-backend-2/blob/deploy/results/1.jpg?raw=true)


## **2번** 
survey에 foobar 필드 추가하여 commit&push, EC2 인스턴스에서 pull후 `deploy.sh` 실행 결과, 패키치 설치, migration, gunicorn 및 nginx 재시작 등 재배포 시 필요한 동작들이 정확히 수행하는 것을 확인할 수 있습니다.

``` shell
[ec2-user@ip-172-31-2-64 waffle-rookies-19.5-backend-2]$ ./deploy/deploy.sh
Username for 'https://github.com': esc5221
Password for 'https://esc5221@github.com':
remote: Enumerating objects: 86, done.
remote: Counting objects: 100% (86/86), done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 66 (delta 27), reused 66 (delta 27), pack-reused 0
Unpacking objects: 100% (66/66), 30.55 KiB | 2.18 MiB/s, done.
From https://github.com/esc5221/waffle-rookies-19.5-backend-2
 * branch            deploy     -> FETCH_HEAD
   333de83..6c34808  deploy     -> origin/deploy
Updating 333de83..6c34808
Fast-forward

 - 중략 -

 waffle_backend/settings.py                                                        |  32 ++++++++++++++++++++++----------
 48 files changed, 23 insertions(+), 10 deletions(-)
Requirement already satisfied: asgiref==3.4.1 in ./venv0/lib/python3.8/site-packages (3.4.1)
WARNING: You are using pip version 20.2.3; however, version 21.3.1 is available.
You should consider upgrading via the '/home/ec2-user/waffle-rookies-19.5-backend-2/venv0/bin/python3 -m pip install --upgrade pip' command.

- 중략 - 

Migrations for 'survey':
  survey/migrations/0003_operatingsystem_foobar.py
    - Add field foobar to operatingsystem
System check identified some issues:

Running migrations:
  Applying survey.0003_operatingsystem_foobar... OK
System check identified some issues:

- 중략 - 

System check identified 5 issues (0 silenced).
8000/tcp:             3558  3560
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
Redirecting to /bin/systemctl restart nginx.service
[ec2-user@ip-172-31-2-64 waffle-rookies-19.5-backend-2]$
```

## **3번** 
![Image](https://github.com/esc5221/waffle-rookies-19.5-backend-2/blob/deploy/results/3.jpg?raw=true)