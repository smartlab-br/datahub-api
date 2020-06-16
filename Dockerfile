FROM smartlab/flask-dataviz:latest
LABEL maintainer="smartlab-dev@mpt.mp.br"

USER root

COPY --chown=uwsgi:uwsgi start.sh* /
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt && chmod +x /start.sh

USER uwsgi

COPY app /app/
COPY uwsgi.ini* /etc/uwsgi/conf.d/

ENTRYPOINT ["sh", "/start.sh"]
