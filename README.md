# 와플스튜디오 Backend Seminar[2] 과제

## esc5221 / 최병욱
_________________________________________


### ㄹㄷ 
- 
- `waffle-rookies-19.5-backend-2`의 `README.md`에 과제 관련 하고 싶은 말, 어려웠던 점 등을 남겨주세요. 물론 적극적으로 해결되어야 할 피드백이나
질문 사항은 [Issues](https://github.com/wafflestudio/19.5-rookies/issues) 등을 이용해주세요!
- `GET /api/v1/seminar/` API에 관련해, Django Debug Toolbar를 이용하여 query를 보고 스크린샷과 함께 느낀 점이나 이를 통해 조금이라도 query를 개선한 부분을 남겨주세요.
물론 다른 API들에 대해서 추가적으로 포함하셔도 좋습니다.
- 개발 과정의 흐름이나 시행 착오를 알아보기 좋게 작성해주셔도 좋습니다.
- 구현을 하다가 과제 내용에 명시되지 않은 경우가 있다고 생각되면 [Issues](https://github.com/wafflestudio/19.5-rookies/issues) 에서 질문해주세요.


![스크린샷 2020-08-30 02 12 24](https://user-images.githubusercontent.com/35535636/91642533-097dec80-ea67-11ea-96e4-ab0dfa757187.png)

1. 개설 후 Settings > Manage access 로 들어갑니다.

![스크린샷 2020-08-30 02 13 52](https://user-images.githubusercontent.com/35535636/91642567-5eb9fe00-ea67-11ea-9382-89fcce03be70.png)

3. collaborator로, 세미나 운영진들을 초대합니다.

![스크린샷 2020-08-30 02 14 59](https://user-images.githubusercontent.com/35535636/91642588-87da8e80-ea67-11ea-9d5a-60a3596463c9.png)

- [@Jhvictor4](https://github.com/Jhvictor4) 
- [@gina0605](https://github.com/gina0605)
- [@dodo4114](https://github.com/dodo4114)
- [@PFCjeong](https://github.com/PFCJeong)

![스크린샷 2020-08-30 02 16 17](https://user-images.githubusercontent.com/35535636/91642619-cbcd9380-ea67-11ea-84ea-1a0729103755.png)

4. 아래 스크린샷과 같은 directory 구조를 갖추어야 합니다.

```
/README.md
/.gitignore
/waffle_backend/manage.py
/waffle_backend/waffle_backend/*
/waffle_backend/survey/*
/waffle_backend/user/*
...
```

![스크린샷 2020-08-30 03 16 21](https://user-images.githubusercontent.com/35535636/91643553-3b934c80-ea6f-11ea-8e5c-c20b1e6e42a3.png)

![스크린샷 2020-08-30 03 16 29](https://user-images.githubusercontent.com/35535636/91643554-3cc47980-ea6f-11ea-9ade-087b4845df11.png)

5. 가급적 repository 생성과 collaborator 지정은 미리 해둬주세요! 제출 방식을 다들 올바로 이해하고 계신지와 함께, 가능하다면 대략적인 진행상황을 보면서 필요하면 몇 가지 말씀을 더 드릴 수도 있습니다.


6. 과제 진행은 다음 절차를 따라주세요

  - 현재 디렉토리에 있는 [waffle_backend](waffle_backend) 를 clone 후 waffle-rookies-19.5-backend-2 에 복사합니다.
  - **waffle-rookies-19.5-backend-2 디렉토리에서 `git checkout -b workspace` 로 이번 과제를 진행할 새로운 브랜치를 만들고 이동합니다**<br>Git Desktop과 같은 GUI 툴을 사용하신다면 workspace라는 이름으로 New branch를 생성해주세요.
  - 해당 branch에서 작업을 완료해주세요. (**master branch에 push하면 안됩니다. git push origin workspace로 workspace branch에만 변경사항을 업로드해주세요.**)
  - 과제를 마치셨으면 마지막으로 workspace branch에 push 해주시고 Pull Request를 날려주시면 됩니다. (master <- workspace)
  - 만약 master에 변경사항을 업로드한 경우 workspace branch에서 `git merge master`를 통해 master의 변경사항을 workspace branch로 가져오고 `git checkout master`를 이용해 master branch로 이동 <br>
    ```
    git revert --no-commit HEAD~1..
    git commit
    git push origin master
    ```
    를 이용해 commit을 돌리시면 됩니다. (HEAD~ 뒤의 숫자는 되돌릴 commit의 수)
  - git이 어려운 경우 [OT자료](../../wafflestudio%2018.5%20rookies%20OT.pdf), https://backlog.com/git-tutorial/kr/stepup/stepup1_1.html 등을 참고해주세요.

7. 제출 기한 전까지 PR을 완료하고 API CALL을 해주시면, 지정된 세미나 운영진들이 확인할 것입니다. GitHub repository에 반영되도록 commit, push해두는 것을 잊지 마세요.

8. master branch의 상태는 반드시 [skeleton code](waffle_backend)와 동일해야합니다. 

## 참고하면 좋은 것들 !!! 읽어보세요
- 추후 점진적으로 추가 예정입니다.
- https://www.django-rest-framework.org/api-guide/requests/#query_params
- https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
- https://www.django-rest-framework.org/api-guide/generic-views/#generic-views
- https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself

- 앞으로도 늘 그렇겠지만, 과제를 진행하며 모르는 것들과 여러 난관에 부딪히리라 생각됩니다. 당연히 그 지점을 기대하고 과제를 드리는 것이고, 기본적으로 스스로 구글링을
통해 여러 내용을 확인하고 적절한 수준까지 익숙해지실 수 있도록 하면 좋겠습니다.
- [Issues](https://github.com/wafflestudio/19.5-rookies/issues) 에 질문하는 것을 어려워하지 마시길 바랍니다. 필요하다면 본인의 환경에 대한 정보를 잘 포함시켜주세요.
또한 Issue 제목에 과제 내용의 번호 등을 사용하시기보다, 궁금한 내용의 키워드가 포함되도록 해주세요. 답이 정해져있지 않은 설계에 대한 고민 공유도 좋습니다.
- 문제를 해결하기 위해 질문하는 경우라면, 질문을 통해 기대하는 바, (가급적 스크린샷 등을 포함한) 실제 문제 상황, 이를 해결하기 위해 시도해본 것, 예상해본 원인 등을 포함시켜 주시는 것이 자신과 질문을 답변하는 사람, 제3자 모두에게 좋습니다.
- 저는 직장을 다니고 있으므로 아주 빠른 답변은 어려울 수 있고, 특히 과제 마감 직전에 여러 질문이 올라오거나 하면 마감 전에 모든 답변을 드릴 수 있다는 것은
보장하기 어렵다는 점 이해해주시면 좋겠습니다. 그리고 세미나 진행자들이 아니어도, 참여자 분들 모두가 자신이 아는 선에서 서로 답변을 하고 도우시려고 하면 아주 좋을 것 같습니다.
- 과제의 핵심적인 스펙은 바뀌지 않을 것이며 설령 있다면 공지를 따로 드릴 것입니다. 하지만 문구나 오타 수정 등의 변경은 수시로 있을 수 있고,
특히 '참고하면 좋을 것들'에는 추가 자료들을 첨부할 수도 있습니다. 때문에 종종 이 repository를 pull 받아주시거나, 이 페이지를 GitHub에서 종종 다시 확인해주시기 바랍니다.
