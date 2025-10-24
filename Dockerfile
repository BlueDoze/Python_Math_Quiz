FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements if present and install (no-op if not provided)
COPY requirements.txt /app/requirements.txt
RUN set -eux \
	&& if [ -f /app/requirements.txt ] && [ "$(wc -c < /app/requirements.txt)" -gt 0 ]; then \
		pip install --no-cache-dir -r /app/requirements.txt; \
	fi

# Copy the application source
COPY . /app

# Ensure output is not buffered (helps logging)
ENV PYTHONUNBUFFERED=1

# Default command to run the quiz
CMD ["python", "Pedro_Aguiar_Python_Math_Quiz_Code.py"]
