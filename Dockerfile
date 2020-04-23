FROM smartlab/flask-dataviz:development
LABEL maintainer="smartlab-dev@mpt.mp.br"

ENV PYTHONPATH /app:/usr/lib/python3.8/site-packages

COPY requirements.txt /app/requirements.txt
COPY app/*.py /app/
COPY uwsgi.ini /etc/uwsgi/conf.d/
# COPY start.sh /start.sh

ENV MPLLOCALFREETYPE 1

WORKDIR /app

RUN pip3 install -r /app/requirements.txt && \
    rm -rf /var/cache/apk/* && \
    rm -rf ~/.cache/
# # RUN webdrivermanager firefox chrome --linkpath /usr/local/bin

ENV LANG C.UTF-8
ENV DEBUG 0
ENV FLASK_APP /app/main.py

COPY app /app/

EXPOSE 5000

ENTRYPOINT ["sh", "/start.sh"]