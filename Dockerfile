FROM python:3.9-slim

COPY    ./tools /tools

RUN    pip3 install -r tools/requirements.txt

CMD    python3 tools/server.py