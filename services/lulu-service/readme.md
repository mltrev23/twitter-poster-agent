# Lulu Service

This is the `lulu-service` which is a part of the Botify project. It is built using FastAPI.

## Endpoints

### GET /lulu-service

Returns a simple JSON response.

#### Response

```json
{
  "Hello": "World"
}
```

## Running the Service

To run the service, use the following command:

```bash
uvicorn main:app --reload
```

Make sure you are in the `services/lulu-service` directory when running the command.