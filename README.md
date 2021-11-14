# 와플스튜디오 Backend Seminar[5] 과제

## esc5221 / 최병욱
_________________________________________


## **1번** 
* ErrorLog 모델을 아래와 같이 설정하고, custom exception_handler를 만들어, error 발생 시 error log가 자동으로 기록되도록 하였습니다. 구현 결과 db상에 error log가 잘 수집된 것을 확인할 수 있습니다.

  ![Image](https://github.com/esc5221/waffle-rookies-19.5-backend-2/blob/final/results/1.JPG?raw=true)


## **2번** 
* HTTP_500_INTERNAL_SERVER_ERROR의 경우, exception_handler의 parameter exc에 "status_code" attribute가 없다는 점을 이용해 500 error를 처리하고, "status_code" attribute가 있는 경우에는 기존 rest_framework에서 제공하는 exception_handler를 사용하도록 하였습니다.

  ![Image](https://github.com/esc5221/waffle-rookies-19.5-backend-2/blob/final/results/2.JPG?raw=true)

## **3번** 

  ![Image](https://github.com/esc5221/waffle-rookies-19.5-backend-2/blob/final/results/3.JPG?raw=true)


## 소감
* 과제 1~5를 진행하며 django/django_rest 프레임워크, RDBMS, REST API의 개념, test 및 CI, amazon AWS/RDS 사용 및 서버 배포 등을 배워갈 수 있었습니다. Backend에서 처리해야하는 task들을 전반적으로 알아봤지만, 세부적으로 파고들면 배울게 정말 많다고 느꼈습니다. 또한 과제는 혼자서 진행하기 때문에, 협업으로 진행할 시 고려해야할 점들도 배워나가야할 것 같습니다. 과제를 통해 얻은 기본기를 가지고, 토이 프로젝트에서 협업으로 프로젝트를 진행하는 방법을 익혀봐야겠습니다. 세미나 진행하시느라 고생많으셨습니다. 감사합니다.