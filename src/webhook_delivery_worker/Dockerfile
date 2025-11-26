FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN echo "requirements.txt:"
RUN echo "------------"
RUN cat requirements.txt
RUN echo "------------"
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setup Entrypoint
COPY entrypoint.sh /entrypoint.sh
# Fix potential Windows line endings (CRLF) issues
RUN sed -i 's/\r$//' /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Setup master/slave wrapper
COPY wrapper.sh /wrapper.sh
# Fix potential Windows line endings (CRLF) issues
RUN sed -i 's/\r$//' /wrapper.sh && \
    chmod +x /wrapper.sh

EXPOSE 5000

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]

# CMD is passed as arguments to the ENTRYPOINT script
CMD ["/wrapper.sh"]
