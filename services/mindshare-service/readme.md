# Botify Mindshare Service

This is the Mindshare Service for the Botify project, built using FastAPI.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/botify.git
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

## Running the Service

1. Navigate to the service directory:
    ```bash
    cd botify/services/mindshare-service
    ```

2. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

3. Open your browser and go to `http://127.0.0.1:8000/mindshare-service` to see the service in action.

## Endpoints

- `GET /mindshare-service`: Returns a simple JSON response.

## License

This project is licensed under the MIT License.