# Realtime

## 실행
Docker와 MongoDB를 반드시 설치해야 됩니다.

### `monitor`
`monitor`는 서버의 성능을 MongoDB로 보고하는 모듈입니다. 다음과 같이 Docker Image로 빌드 후 실행하면 됩니다.

```
$ cd monitor
$ docker build -t amd/monitor:1.0.0 .
$ docker run -d amd/monitor:1.0.0
```

### `classifier`
`classifier`는 수집한 파일을 분석하여 MongoDB로 보고하는 모듈입니다. 다음과 같이 Docker Image로 빌드 후 실행하면 됩니다. 환경 변수를 상황에 맞춰 수정해야 됩니다.

```
$ cd classifier
$ docker build -t amd/classifier:1.0.0 .
$ docker run -d \
  -e API_URL="http://localhost:8000" \
  -e MONGO_HOST="localhost" \
  -e MONGO_PORT=27017 \
  -e MONGO_USERNAME="root" \
  -e MONGO_PASSWORD="example" \
  -e MONGO_DB="malware" \
  -v /path/to/local/folder:/data \
  amd/classifier:1.0.0
```
