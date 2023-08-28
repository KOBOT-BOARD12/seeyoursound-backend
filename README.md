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
### 4. How to set
* #### 터미널에서 실행할 명령어
```python
git clone https://github.com/KOBOT-BOARD12/seeyoursound-backend.git
```
```python
pip install -r requirements.txt
```
* #### ENV
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
### 5. How to run
```python
uvicorn app:app --host=0.0.0.0 --port={port}
```