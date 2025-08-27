FROM python:3.12-slim

WORKDIR /app

# Install hyperon
RUN pip install hyperon

# Set up a shell by default
CMD ["/bin/bash"]