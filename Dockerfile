FROM python:3
COPY . /workflows
WORKDIR /workflows
RUN pip install -r pip-requirements-test.txt
RUN pip install .[test]
ENTRYPOINT ["pytest"]
CMD ["src"]