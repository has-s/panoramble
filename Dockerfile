# используем облегчённый Python 3.12
FROM python:3.12-slim

# рабочая директория внутри контейнера
WORKDIR /backend

# копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код приложения
COPY backend ./backend

# открываем порт uvicorn
EXPOSE 8000

# команда запуска FastAPI
CMD ["uvicorn", "backend.main:backend", "--host", "0.0.0.0", "--port", "8000"]