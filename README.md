# 와플스튜디오 Backend Seminar[4] 과제

## esc5221 / 최병욱
_________________________________________

- Public IPv4 address: http://3.12.74.177
- HTTP Domain: http://wafl.shop

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

## 느낀점
* 서버에서 환경 설정을 일일히 하는게 상당히 고역이라는 점이 느껴졌습니다. 특히 EC2에서 mysql을 mariadb로 사용하는 것 떄문에 혼동이 있어 시간을 잡아먹었던 것 같습니다. 나머지는 대부분 이전 과제를 진행하며 만나본 오류들이어서 방법을 알고 디버깅할 수 있었지만, 그래도 환경 설정이 쉽지는 않은 것 같습니다. 
* 환경 설정 도중, 실수로 일반 유저에게 루트 디렉토리의 권한을 부여해 루트 볼륨을 날리고 새로 환경 설정을 하게 되었습니다. 스냅샷을 찍어놓았으면 좋았겠다는 생각이 들었습니다.
* settings.py에서 database 지정 시, test와 test가 아닐 때 다르게 지정되도록 설정하였습니다. test시에는 local db에서 해도 상관없기 때문에, local db로 설정하고, 그 외의 경우에는 RDS의 db를 사용하도록 설정했습니다. 통상적으로 이런 식의 설정을 사용하는지 궁금했습니다.
* 과제 3번에서 도메인 등록을 진행했는데, 노트북에서 도메인 접속이 불가능했습니다. 등록이 제대로 된 건지 확인해보려 nameserver를 지정해 nslookup으로 접속이 되는 것을 확인하고, https://www.whatsmydns.net/에서도 체크를 해보았으나 정상적으로 전파가 된 것을 확인했습니다. 스마트폰을 이용해 lte로 접속하니, 통신사 쪽 네임서버에는 등록이 되어 접속이 잘 되었지만, 노트북은 학교에서 관리하는 네트워크를 사용했기 때문에 학교 쪽 네임서버에는 아직 전파가 안된 것이라고 추측했습니다. 네트워크 과목에서 배운 개념들을 실제로 접해본 좋은 경험이었던 것 같습니다.