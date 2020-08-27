FROM python:3
COPY . /workflows
WORKDIR /workflows
RUN pip install pytest
ENTRYPOINT ["pytest"]
CMD ["src"]