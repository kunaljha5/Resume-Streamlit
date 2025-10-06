FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.23 /uv /uvx /usr/local/bin/

WORKDIR /app

ADD . /app

RUN uv sync --locked --no-dev

EXPOSE 8501

ENV PATH="/app/.venv/bin:$PATH"

CMD ["streamlit", "run", "src/resume_streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0" ]