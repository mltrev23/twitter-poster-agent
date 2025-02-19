# Botify Project

This project contains multiple services built using FastAPI. Each service is designed to handle specific functionalities within the Botify ecosystem.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd botify
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Services

### Query Service

To run the Query Service, use the following command:
```bash
uvicorn services.query-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/query-service`.

#### Endpoints

- `GET /query-service`: Returns a simple JSON response with "Hello" and "World".

### Mindshare Service

To run the Mindshare Service, use the following command:
```bash
uvicorn services.mindshare-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/mindshare-service`.

#### Endpoints

- `GET /mindshare-service`: Returns a simple JSON response.

### Lulu Service

To run the Lulu Service, use the following command:
```bash
uvicorn services.lulu-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/lulu-service`.

#### Endpoints

- `GET /lulu-service`: Returns a simple JSON response.

## License

This project is licensed under the MIT License.
