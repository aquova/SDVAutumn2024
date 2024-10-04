FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY . /autumn
WORKDIR /autumn
RUN uv sync --frozen
CMD ["uv", "run", "main.py"]
