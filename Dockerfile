FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Expose the port your app will run on
EXPOSE 8008

# Configure pip to avoid timeouts
RUN mkdir -p /etc/pip && echo "[global]\ntimeout = 180\nindex-url = https://pypi.org/simple" > /etc/pip/pip.conf

# Copy only dependency files first to leverage Docker cache
COPY pyproject.toml ./

# Install all dependencies
RUN pip install --upgrade pip && pip install -e .

# Now copy the rest of the project files
COPY . .

# Set the default command to run the bot
CMD ["python", "bot.py"]
