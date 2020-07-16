FROM smartlab/flask-dataviz:latest
LABEL maintainer="smartlab-dev@mpt.mp.br"

USER root

# If you need to tune start.sh, uncomment the following line
#COPY --chown=uwsgi:uwsgi start.sh / 
COPY requirements.txt /app/requirements.txt
COPY app/test/requirements.txt /app/requirements_qa.txt

RUN pip3 install -r /app/requirements.txt && \
    pip3 install -r /app/requirements_qa.txt && \
    mkdir /report && \
    chown -R uwsgi:uwsgi /report && \
    chmod +x /start.sh

USER uwsgi

COPY app /app/
# If you need to tune uwsgi, uncomment the following line
#COPY uwsgi.ini /etc/uwsgi/conf.d/

ENTRYPOINT ["sh", "/start.sh"]
