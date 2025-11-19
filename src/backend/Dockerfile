FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setup Entrypoint
COPY entrypoint.sh /entrypoint.sh
# Fix potential Windows line endings (CRLF) issues
RUN sed -i 's/\r$//' /entrypoint.sh && \
    chmod +x /entrypoint.sh

EXPOSE 5000

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]

# CMD is passed as arguments to the ENTRYPOINT script
CMD ["flask", "run", "--host=0.0.0.0"]
