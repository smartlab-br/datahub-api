FROM smartlab/flask:latest
LABEL maintainer="smartlab-dev@mpt.mp.br"

COPY app /app/
COPY uwsgi.ini /etc/uwsgi/

EXPOSE 5000
WORKDIR /app

ENTRYPOINT ["sh", "/start.sh"]
