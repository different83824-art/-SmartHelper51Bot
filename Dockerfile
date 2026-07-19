# Use a full Python image instead of slim to ensure all build headers are present
FROM python:3.11

# Install system dependencies and Rust compiler
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Rust to the system path permanently
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Upgrade pip and install maturin first so Python knows how to build the library
RUN pip install --no-cache-dir --upgrade pip setuptools wheel maturin

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot code
COPY . .

# Run the bot
CMD ["python", "bot.py"]
