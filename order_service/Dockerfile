FROM python:3.11-slim

WORKDIR /app

# 先複製 shared-models 目錄
COPY shared-models/ /app/shared-models/

# 複製 requirements.txt 並安裝依賴
COPY order_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製訂單服務的其他文件
COPY order_service/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]