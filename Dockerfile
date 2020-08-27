FROM python:3
COPY . /workflows
WORKDIR /workflows
RUN pip install .[test]
ENTRYPOINT ["pytest"]
CMD ["src"]