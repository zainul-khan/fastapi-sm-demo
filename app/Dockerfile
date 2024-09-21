FROM python:3.12-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./*.py /code/
COPY ./routers/*.py /code/routers/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]