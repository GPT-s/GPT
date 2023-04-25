# 베이스 이미지를 명시
FROM ubuntu

# 추가적으로 필요한 파일들을 다운로드

# Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# main.py 파일을 컨테이너에 복사
COPY main.py /

# 'src' 모듈 설치
RUN apt-get install -y python3-pip

# 컨테이너 시작시 실행될 명령어

CMD [ "python3", "/main.py" ]