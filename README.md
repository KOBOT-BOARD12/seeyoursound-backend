# 👀🔉 See Your Sound
<ㄱ 림>
### 🔧 개발 배경
#### 청각 장애인과 길에서 이어폰을 끼고 다니는 즉, 외부 소리가 차단된 사람들이 도로 환경에서 발생하는 소리들을 인식하도록 하는 장치가 필요하다고 생각했다.
### 🔦 개발 목적
#### 소리를 실시간으로 인식 후, 디스플레이 알림과 진동으로 소리의 종류나 미리 등록된 키워드 여부, 소리의 방향을 알려 주는 서비스를 만드는 것이 목적이다.
### 🎉  See Your Sound App 실행 순서
0. 레포지토리 다운로드 - 중앙 서비스 서버
```
git clone https://github.com/KOBOT-BOARD12/seeyoursound-backend.git
```
1. 레포지토리 다운로드 - 모델 서버 `(※ gpu가 탑재돼 있는 환경에서 실행시키는 것이 안정적입니다.)`
```
https://github.com/KOBOT-BOARD12/seeyoursound-model-serving.git
```
2. 중앙 서비스 서버와 모델 서버를 실행시킨다. 
```shell
uvicorn app:app --port={$port}
```
3. SeeYourSound App을 실행시켜 회원가입 후 알림을 받을 클래스를 선택하고, 필요한 키워드를 등록시킨다.
4. 주변 소리를 차단한 뒤 길을 걸으며 테스트한다. (...)

---
# 팀원 소개 및 역할
1. 👨‍💻 윤민상

- Position : 팀장
- Github: <https://github.com/minsang22>
- Email : nornen20@kookmin.ac.kr
- Role
  - 모델 개발 및 서빙

2. 🌖 성창엽

- Position : 팀원
- Github: <https://github.com/scy6500>
- Email : scy6500@kookmin.ac.kr
- Role
  - 서버 개발 및 모델 개발

3. 🖤 안수현

- Position : 팀원
- Github: <https://github.com/3uhyeon>
- Email : saker123456@kookmin.ac.kr
- Role
  - 모바일 앱

4. 🧑🏻‍💻 김영석

- Position : 팀원
- Github: <https://github.com/youngseok0>
- Email : kys030908@kookmin.ac.kr
- Role
  - 모델 개발 및 서빙

5. 🫨 신수민

- Position : 팀원
- Github: <https://github.com/syngrxm>
- Email : 5luck21948@kookmin.ac.kr
- Role
  - 서버 개발
---
# Project 'SeeYourSound' Backend
### 1. 'SeeYourSound'에서의 백엔드
#### App과 Model Server 그리고 Firebase와의 원활한 연결, API 개발 부분을 맡았다.
---
### 2. 'SeeYourSound' 백엔드 개발 환경
#### Ubuntu 22.04.3 버전에서 개발을 진행하였다. 주 개발 환경은 Python 3.10.12 버전을 사용하였다.
---
### 3. 'SeeYourSound' 백엔드의 구조
#### a. [Manager](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/manager/firebase_manager.py): Manager Folder - Firebase Firestore와 연동한다.
#### b. [Keyword](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/router/keyword_router.py): Keyword Router - App에서 Keyword 등록, 리턴, 삭제 API를 호출하여 Keyword를 관리할 수 있도록 해 준다.
#### c. [Return Model Data](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/router/model_router.py): Model Data Return Router - 사용자의 개별 키워드들 모델 가중치를 받아 Firebase Storage에 저장해 준다.
#### d. [Websoket](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/router/websocket.py): Websocket Entire Manager - 사용자의 기기로부터 앱을 통해 들어오는 소리를 실시간 스트리밍한다.
---
### 4. How to set (without Docker)
* #### repository clone 받기
```shell
git clone https://github.com/KOBOT-BOARD12/seeyoursound-backend.git
```
* #### Python 가상 환경 설정
```shell
python -m venv .venv
```
```shell
. .venv/bin/activate
```
* #### 필요한 package 설치
```shell
pip install -r requirements.txt
```
* #### Install sox (on Linux)
```shell
apt-get install libsox-fmt-all
```
```shell
apt-get install sox
```
```shell
pip install sox
```
* #### Install sox (on Mac)
```shell
brew install sox --with-lame --with flac --with-libvorbis
```
```shell
brew install sox
```
```shell
pip install sox
```
### 5. How to set (with Docker)
```shell
docker build backend .
```
```
docker run -p 8000:8000 backend
```

### 6. ENV
```
TYPE
PROJECT_ID
PRIVATE_KEY_ID
PRIVATE_KEY
CLIENT_EMAIL
CLIENT_ID
AUTH_URI
TOKEN_URI
AUTH_PROVIDER_X509_CERT_URL
CLIENT_X509_CERT_URL
UNIVERSE_DOMAIN
MODEL_SERVER_URL
```
---
### 7. How to run
```python
uvicorn app:app --host=0.0.0.0 --port={$port}
```