FROM python:3.11-slim-bullseye

WORKDIR /aioplus/

RUN apt-get update \
    && apt-get install --no-install-recommends --yes make \
    && apt-get clean

COPY pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==2.1.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-interaction --no-root --with lint,test

COPY ./ ./

ENTRYPOINT [ "python" ]
CMD [ "--version" ]
