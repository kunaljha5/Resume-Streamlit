FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.23 /uv /uvx /bin/

WORKDIR /app

ADD . /app

RUN uv sync --locked --no-dev

EXPOSE 8501


CMD ["uv", "run", "streamlit", "run", "src/resume_streamlit/main.py" ]