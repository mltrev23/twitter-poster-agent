# Botify Project

This project contains multiple services built using FastAPI. Each service is designed to handle specific functionalities within the Botify ecosystem.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd botify
    ```

2. Install the dependencies:
    ```bash
    poetry install --no-root
    ```

## Running the Services

### Query Service

To run the Query Service, use the following command:
```bash
poetry run uvicorn services.query-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/query-service`.

#### Endpoints

- `GET /query-service`: Returns a simple JSON response with "Hello" and "World".

### Mindshare Service

To run the Mindshare Service, use the following command:
```bash
poetry run uvicorn services.mindshare-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/mindshare-service`.

#### Endpoints

- `GET /mindshare-service`: Returns a simple JSON response.

### Lulu Service

To run the Lulu Service, use the following command:
```bash
poetry run uvicorn services.lulu-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/lulu-service`.

#### Endpoints

- `GET /lulu-service`: Returns a simple JSON response.

## Managing project with poetry

1. Install a new module
    ```bash
    poetry add <module-name>
    ```

2. Remove a module
    ```bash
    poetry remove <module-name>
    ```

3. Update a module
    ```bash
    poetry update <module-name>
    ```

4. Running commands
    ```bash
    poetry run <command>
    ```

## License

This project is licensed under the MIT License.
