FROM python:3.11-slim AS qa
WORKDIR /workspace
COPY tests ./tests
COPY scripts ./scripts
COPY conf ./conf
RUN pip install --no-cache-dir pytest && pytest tests -q

FROM openhab/openhab:4.2.1
LABEL org.opencontainers.image.title="OpenHAB CI/CD Lab"
LABEL org.opencontainers.image.description="Practice repository for OpenHAB validation, testing and delivery"
WORKDIR /openhab
COPY --from=qa /workspace/conf /openhab/conf
EXPOSE 8080
