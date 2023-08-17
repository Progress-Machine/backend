FROM python:3.10.12

WORKDIR /app


COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "5000"]
