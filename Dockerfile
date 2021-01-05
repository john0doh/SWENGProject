FROM python:3.9.1-slim-buster
ADD actual1.py /
RUN pip install pyGitHub
RUN pip install bokeh
RUN pip install pandas
CMD [ "bokeh", "serve", "actual1.py" ]