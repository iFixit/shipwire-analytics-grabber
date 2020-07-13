FROM alpine:latest

# Install node, python3, and dev dependencies for node-gyp
RUN      apk update && apk add python3 && mkdir -p /opt/shipwire-analytics-grabber

COPY . /opt/shipwire-analytics-grabber
WORKDIR  /opt/shipwire-analytics-grabber

# Install python project, install modules
RUN      python3 -m ensurepip \
          && pip3 install --upgrade pip \
          && pip3 install -r requirements.txt

ENTRYPOINT python3 shipwire-grabber.py
