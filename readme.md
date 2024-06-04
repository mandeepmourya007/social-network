# Django Project with Docker Compose

This is a Django project template configured to run with Docker Compose. It includes Dockerfiles for both development and production environments.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

## Setup

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/mandeepmourya007/social_network.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social_network
    ```

3. Build the Docker image:

    ```bash
    docker-compose build
    ```

4. Start the Docker container:

    ```bash
    docker-compose up
    ```

5. Open your web browser and navigate to `http://localhost:8000` to view the Django project.

## Project Structure

- `Dockerfile`: Dockerfile for the development environment.
- `docker-compose.yml`: Docker Compose configuration file.
- `requirements.txt`: Python dependencies for the project.
- `social_network/`: Django project directory.
- `api/`: Django app directory.

## Configuration

- Database: By default, the project uses SQLite for development. You can modify the `DATABASE_URL` environment variable in the `docker-compose.yml` file to use a different database.
- Django settings: You can configure Django settings in the `settings.py` file inside the `social_network` directory.

## Development

For development, you can run the Django development server directly using Docker Compose. Changes to your code will be automatically reflected without needing to rebuild the Docker image.

```bash
docker-compose up
