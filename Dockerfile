# Base 이미지 설정
# FROM ubuntu:20.04
FROM --platform=linux/amd64 python:3.9

# 디비 정보
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MySQL_HOST=project-db-stu.ddns.net \
    MySQL_PORT=3307 \
    MySQL_USER=smhrd_e_3 \
    MySQL_PASSWORD=smhrde3 \
    MySQL_DB=smhrd_e_3

# 작업 디렉토리 설정
WORKDIR /root/GPT

# 필요한 파일들 복사
COPY main.py /root/GPT/main.py
#COPY .env /root/GPT/.env
COPY requirements.txt /root/GPT/requirements.txt
COPY src /root/GPT/src/

ENV DEBIAN_FRONTEND=noninteractive

# 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y python3 wget unzip && \
    pip install selenium requests -r requirements.txt schedule

#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
#RUN apt-get update

# CHROME 운영체제
RUN case "$(uname -s)" in \
        Linux*) \
            wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
            sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list' && \
            apt-get update && \
            apt-get install -y google-chrome-stable ;; \
        *) \
            curl https://dl-ssl.google.com/linux/linux_signing_key.pub --remote-name && \
            apt-get update && \
            apt-get install -y gnupg && \
            apt-key add linux_signing_key.pub && \
            sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list' && \
            apt-get update && \
            apt-get install -y google-chrome-stable ;; \
    esac


# 운영체제에 따라 크롬 드라이버 다운로드
RUN case "$(uname -s)" in \
        Linux*) \
            apt-cache policy google-chrome-stable | sed -n -e 's/\*\*\([0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+\)/\1/p' | xargs -I {} sh -c 'wget -O /root/GPT/chromedriver.zip https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip && unzip /root/GPT/chromedriver.zip chromedriver -d /root/GPT/'; \
            ;; \
        Darwin*) \
            wget -O /root/GPT/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64.zip && unzip /root/GPT/chromedriver.zip chromedriver -d /root/GPT/; \
            ;; \
        *) \
            wget -O /root/GPT/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_win32.zip && unzip /root/GPT/chromedriver.zip chromedriver -d /root/GPT/; \
            ;; \
    esac

ENV DISPLAY=:99

#COPY crawler.py /root/GPT/crawler.py

# 파이썬 파일 실행
CMD ["python3", "main.py"]