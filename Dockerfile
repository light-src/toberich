# 기본 이미지를 설정합니다. Python 3.9 이미지를 사용합니다.
FROM python:3.9

# 앱 디렉토리를 만들고 Docker 컨테이너 내에서 작업 디렉토리로 설정합니다.
WORKDIR /app

# 현재 디렉토리에 있는 모든 파일을 컨테이너의 작업 디렉토리로 복사합니다.
COPY . /app

# Python 패키지를 업데이트 합니다.
RUN pip install --upgrade pip
# 필요한 Python 패키지를 설치합니다.
RUN pip install -r requirements.txt

# Flask 애플리케이션을 실행합니다.
CMD ["python", "app.py", ">&", "log-${date}.txt"]