FROM python:3.10.12

WORKDIR /app


COPY . .
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "5000"]
