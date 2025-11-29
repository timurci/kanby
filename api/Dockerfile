FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --group api

COPY kanby/ kanby/
COPY api/ api/

EXPOSE 5000

CMD ["uv", "run", "--no-sync", \
    "uvicorn", "api.main:app", \
    "--host", "0.0.0.0", \
    "--port", "5000", \
    "--log-level", "debug"]