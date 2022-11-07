FROM python:3.10-slim-buster

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app
VOLUME /app/logs

COPY biligank_flask biligank_flask/

COPY serve.sh app_configs.py ./
RUN chmod +x ./serve.sh

EXPOSE 7771

CMD ["bash", "./serve.sh"]
