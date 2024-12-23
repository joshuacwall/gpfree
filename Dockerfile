FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*


# Copy application
COPY . .

# Install Python packages
RUN pip3 install -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Health check to verify the service is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
