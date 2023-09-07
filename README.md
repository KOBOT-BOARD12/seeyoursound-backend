# Project 'SeeYourSound' Backend

### 1. 'SeeYourSound'에서의 백엔드

App과 Model Server 그리고 Firebase와의 연결, API 개발 부분을 맡았다.
<br>

### 2. 'SeeYourSound' 백엔드 개발 환경

Ubuntu 22.04.3, Python 3.11.1 버전에서 개발을 진행하였다.
<br>

### 3. 'SeeYourSound' 백엔드의 구조

a. [Manager](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/manager/firebase_manager.py): Manager Folder - Firebase Firestore와 연동한다.

b. [Keyword](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/router/keyword_router.py): Keyword Router - App에서 Keyword 등록, 리턴, 삭제 API를 호출하여 Keyword를 관리할 수 있도록 한다.

c. [Websoket](https://github.com/KOBOT-BOARD12/seeyoursound-backend/blob/develop/router/websocket.py): Websocket Entire Manager - 앱으로부터 들어오는 소리를 websocket 연결을 통해 실시간 스트리밍한다.
<br>

### 4. ENV

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

<br>

### 5-1. How to install (without Docker)

- Firebase 프로젝트 생성 (모델 백엔드와 동일한 Firebase 프로젝트 사용)
  - [공식 문서](https://firebase.google.com/)에 따라 Firebase 프로젝트를 생성한다.
  - ENV 항목을 참고하여 .env 파일을 채워서 firebase 세팅 작업을 진행한다.
- repository clone 받기

```shell
git clone https://github.com/KOBOT-BOARD12/seeyoursound-backend.git
```

- Python 가상 환경 설정

```shell
python -m venv .venv
```

```shell
. .venv/bin/activate
```

- 필요한 package 설치

```shell
pip install -r requirements.txt
```

- Install sox (on Linux)

```shell
apt-get install libsox-fmt-all
```

```shell
apt-get install sox
```

```shell
pip install sox
```

- Install sox (on Mac)

```shell
brew install sox --with-lame --with flac --with-libvorbis
```

```shell
brew install sox
```

```shell
pip install sox
```

- 실행

```shell
uvicorn app:app --host=0.0.0.0 --port=8000
```

<br>

### 5-2. How to install (with Docker)

- Firebase 프로젝트 생성 (모델 백엔드와 동일한 Firebase 프로젝트 사용)
  - [공식 문서](https://firebase.google.com/)에 따라 Firebase 프로젝트를 생성한다.
  - ENV 항목을 참고하여 .env 파일을 채워서 firebase 세팅 작업을 진행한다.
- repository clone 받기

```shell
git clone https://github.com/KOBOT-BOARD12/seeyoursound-backend.git
```

- Docker 세팅 후 실행하기

```shell
docker build --tag backend .
```

```shell
docker run -p 8000:8000 backend
```
