FROM python:3.9.1-slim-buster
ADD actual1.py /
COPY requirements.txt /
COPY token.txt /
RUN pip install -r requirements.txt
CMD [ "bokeh", "serve", "actual1.py"]