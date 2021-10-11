# 와플스튜디오 Backend Seminar[3] 과제

## esc5221 / 최병욱
_________________________________________


## **TEST branch**
### **TEST FILES**
- **`user/tests_user.py`**
- **`seminar/tests_sseminar.py`**
### **API List**
- POST /api/v1/signup/
- POST /api/v1/user/login/
- PUT /api/v1/user/me/
- GET /api/v1/user/{user_id}/
- GET /api/v1/user/me/
- POST /api/v1/user/participant/
- POST /api/v1/seminar/
- PUT /api/v1/seminar/{seminar_id}/
- GET /api/v1/seminar/{seminar_id}/
- GET /api/v1/seminar/
- POST /api/v1/seminar/{seminar_id}/user/
- DELETE /api/v1/seminar/{seminar_id}/user/

### **Coverage Report**
<details>
<summary>details for coverage report</summary>

``` 
Name                                                    Stmts Miss Cover
--------------------------------------------------------------------------
manage.py                                                 12    2   83%
seminar/__init__.py                                        0    0  100%
seminar/admin.py                                           1    0  100%
seminar/apps.py                                            4    0  100%
seminar/migrations/0001_initial.py                         6    0  100%
seminar/migrations/0002_userseminar_user.py                7    0  100%
seminar/migrations/0003_auto_20210925_0854.py              4    0  100%
seminar/migrations/0004_alter_userseminar_joined_at.py     4    0  100%
seminar/migrations/0005_auto_20210925_1446.py              6    0  100%
seminar/migrations/0006_seminar_participant_count.py       4    0  100%
seminar/migrations/0007_auto_20210927_1123.py              4    0  100%
seminar/migrations/0008_alter_seminar_online.py            4    0  100%
seminar/migrations/__init__.py                             0    0  100%
seminar/models.py                                         20    0  100%
seminar/serializers.py                                    92    1   99%
seminar/tests.py                                           1    0  100%
seminar/urls.py                                            7    0  100%
seminar/views.py                                         104    3   97%
survey/__init__.py                                         0    0  100%
survey/admin.py                                            4    0  100%
survey/apps.py                                             3    0  100%
survey/management/__init__.py                              0    0  100%
survey/management/commands/__init__.py                     0    0  100%
survey/migrations/0001_initial.py                          6    0  100%
survey/migrations/0002_surveyresult_user.py                7    0  100%
survey/migrations/__init__.py                              0    0  100%
survey/models.py                                          19    0  100%
survey/serializers.py                                     26    8   69%
survey/tests_seminar.py                                  583    3   99%
survey/urls.py                                             8    0  100%
survey/views.py                                           42   21   50%
user/__init__.py                                           0    0  100%
user/admin.py                                              1    0  100%
user/apps.py                                               3    0  100%
user/migrations/0001_initial.py                            8    0  100%
user/migrations/0002_user_role.py                          4    0  100%
user/migrations/0003_auto_20210924_1308.py                 5    0  100%
user/migrations/0004_auto_20210924_1405.py                 5    0  100%
user/migrations/0005_auto_20210925_0531.py                 4    0  100%
user/migrations/0006_alter_instructorprofile_year.py       4    0  100%
user/migrations/0007_alter_participantprofile_accepted.py  4    0  100%
user/migrations/0008_remove_user_is_active.py              4    0  100%
user/migrations/0009_alter_participantprofile_accepted.py  4    0  100%
user/migrations/__init__.py                                0    0  100%
user/models.py                                            53    8   85%
user/serializers.py                                      135   14   90%
user/tests.py                                              1    0  100%
user/tests_user.py                                       224    2   99%
user/urls.py                                               7    0  100%
user/views.py                                             90   14   84%
waffle_backend/__init__.py                                 0    0  100%
waffle_backend/settings.py                                30    0  100%
waffle_backend/urls.py                                     9    0  100%
------------------------------------------------------------------------
TOTAL                                                   1573   76   95%
```

</details>

<br>

