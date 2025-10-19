FROM python:3.11-slim
WORKDIR /app
COPY . .
# Встановлюємо наш пакет
RUN pip install .
# Визначаємо точку входу
ENTRYPOINT ["myuniq"]
CMD ["--help"]