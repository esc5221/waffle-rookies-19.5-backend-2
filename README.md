# 와플스튜디오 Backend Seminar[2] 과제

## esc5221 / 최병욱
_________________________________________


### 과제 완료 
- 저번 과제에서 serializer를 제대로 사용하지 않아, 처음에는 view에서 validation을 구현을 하다가, 나중에 갈 수록 serializer 쪽에 validation을 넣도록 구현하게 되었던 것 같습니다. 과제를 진행할수록 DRF의 feature들에 익숙해지는 것 같았습니다. 배워가면서 코딩을 해서 그런지 코드 일관성이 없이 깔끔하지 못해 아쉬웠습니다... (스파게티 코드)
- create, update 함수에서 serializer를 사용하게 되었을 때, validation 로직이 달라지게 되는 경우가 있을 것 같았습니다 (ex. 세미나 개설 시에는 capacity가 50명 이상이어야 함, 하지만 이후 update에서는 50명 이하로 수정 가능) 이런 경우에 validation 함수 내에서 self.instance가 존재하는지 판단해 분기하였는데, 이렇게 하는게 최선의 방법인지 궁금했습니다.
-  11번에서 요구한 django-debug-toolbar를 사용해 SQL query 분석을 해보았습니다. 기존 구현은 `GET /api/v1/seminar/` API call 시에, participant count를 query를 날려 모두 계산하는 방식을 사용했는데 코드를 짜면서도 participant count를 따로 db에 저장해두면 효율적이라고 생각했지만, 방법을 생각해내기 힘들 것 같아 제쳐두었던 문제였습니다. SQL 분석을 통해 participant count를 따로 계산해두는 방법으로 확실히 query수를 줄일 수 있다는 점을 알 수 있었고, grace day를 이용해 구조를 개선해 `GET /api/v1/seminar/` 호출 시 participant count를 계산하는데 필요한 query를 생략시킬 수 있었습니다. 

    **Before**
![스크린샷 2020-08-30 02 12 24](https://user-images.githubusercontent.com/35535636/91642533-097dec80-ea67-11ea-96e4-ab0dfa757187.png)
    **After**
![스크린샷 2020-08-30 02 12 24](https://user-images.githubusercontent.com/35535636/91642533-097dec80-ea67-11ea-96e4-ab0dfa757187.png)

- Test가 중요하다는 점을 느꼈습니다. 모델을 수정하여 migration을 새로하게 되는 등의 상황이 주어질 때, 원래 잘 작동하던 API도 변화된 환경에서는 작동하지 않을 수 있었습니다. 또한 API 1개만을 test했을 때는 문제가 없어도, 여러 API가 복합적으로 call되면서 db에 CRUD가 지속적으로 일어날 때 발생할 수 있는 문제들을 다루기가 정말 어렵다고 생각했습니다. 과제 3을 진행하며 이런 점들을 많이 고민해봐야겠습니다.
- 모델에 새로운 필드를 추가하여 migration을 새로하게 되면, 기존 db의 row에는 이 필드에 대한 정보가 없어 default값을 주거나, 기존 row들에 따로 값을 넣어주는 로직을 짜야했습니다. 11번에서 query 개선을 진행했을 때, 모델 필드에 participant count를 새로 만들어줬는데, 이때 기존 row들에는 이 값이 존재하지 않아 계산을 해주어야했습니다. 과제에서는 db에 중요한 정보가 없기에 그냥 db 내용을 모두 초기화 하고 기능을 추가했는데, 실제 서비스 운영시에는 이러한 값들을 따로 계산해주는 과정이 필요할 것 같았습니다. 이런 상황을 보통 어떤 식으로 처리하는지 궁금해졌습니다. 