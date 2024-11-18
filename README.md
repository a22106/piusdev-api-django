# qrcode-generator

## Project setup

- 레포지토리 클론
- 가상환경 생성
- 패키지 설치

```bash
pip install -r requirements.txt
```

- 도커 설치

### Local

- DB 설치: `docker run --name postgres-local -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=qrcode -p 5432:5432 -d postgres:latest`


## QRCode Generator

[QRCode Generator Link](https://qrcode.piusdev.com)

## Test

- run integration tests: `python test/run_integration_tests.py`
