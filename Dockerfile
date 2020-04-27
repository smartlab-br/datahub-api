FROM smartlab/flask-dataviz:development
LABEL maintainer="smartlab-dev@mpt.mp.br"

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY app /app/

ENTRYPOINT ["sh", "/start.sh"]