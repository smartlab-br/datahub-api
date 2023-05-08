FROM mptrabalho/datahub-base:1.0.2
LABEL maintainer="smartlab-dev@mpt.mp.br"

COPY requirements.txt /app/requirements.txt

RUN apt-get install -y g++ gcc gfortran libopenblas-dev liblapack-dev --no-install-recommends \
 && pip3 install --no-cache-dir -r /app/requirements.txt \
 && apt-get remove -y g++ gcc gfortran libopenblas-dev liblapack-dev \
 && apt-get clean \
 && chmod +x /start.sh

COPY app /app/

ENTRYPOINT ["sh", "/start.sh"]
