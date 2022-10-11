FROM mptrabalho/datahub-base:1.0.0
LABEL maintainer="smartlab-dev@mpt.mp.br"

# If you need to tune start.sh, uncomment the following line
#COPY --chown=uwsgi:uwsgi start.sh / 
COPY requirements.txt /app/requirements.txt

RUN apt-get install -y g++ gcc gfortran libopenblas-dev liblapack-dev && \
    pip3 install -r /app/requirements.txt && \
    apt-get remove -y g++ gcc gfortran libopenblas-dev liblapack-dev && \
    apt-get clean && \
    chmod +x /start.sh

COPY app /app/
# If you need to tune uwsgi, uncomment the following line
#COPY uwsgi.ini /etc/uwsgi/conf.d/

ENTRYPOINT ["sh", "/start.sh"]
