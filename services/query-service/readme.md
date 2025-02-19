# Botify Query Service

This is a simple FastAPI application that provides a query service endpoint.

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

## Running the Application

To run the FastAPI application, use the following command:
```bash
uvicorn services.query-service.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/query-service`.

## Endpoints

- `GET /query-service`: Returns a simple JSON response with "Hello" and "World".