# XML to JSON Parser REST API

This project provides a REST API built with FastAPI that accepts an XML file as input and returns a JSON file representing the XML structure, using a custom XML parser implemented from scratch (no XML libraries used).

## Features

- Full XML structure preservation in JSON output
- Handles XML declarations, comments, attributes, nested elements, self-closing tags, text content, entity references, and mixed content types
- Exposed as a FastAPI REST endpoint
- Based on pure Python logic; no external XML parsing libraries

## API Endpoints

### `POST /api/xmlToJson`

- **Description**: Convert an uploaded XML file (`.xml`) to its JSON representation.
- **Request**: Upload XML file via multipart/form-data.
- **Response**: JSON structure matching the hierarchy/attributes/content of the uploaded XML file.

#### Example Usage

1. Start the server:
    ```
    uvicorn main:app --reload
    ```
2. Open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Use the provided form to upload your XML file and see the JSON response.

## Setup and Installation

1. Clone the repository:
    ```
    git clone https://github.com/DimpleNaik/xml-to-json.git
    cd xml-to-json-fastapi

    ```
2. Create a virtual environment and activate it:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```
    pip install fastapi uvicorn
    ```
4. To start the server:
    ```
    uvicorn main:app --reload
    ```

## Project Structure

- `main.py`: FastAPI application entry point
- `xml_parser.py`: Custom XML parser logic

## Testing

- Upload various XML files using Swagger UI (`/docs`)
- Review JSON output for correct structure and content mapping


## Frontend (React) Setup and Usage
Node.js and npm installed

The backend FastAPI server running locally (on port 8000 by default)

# Setup React Frontend
Navigate to the frontend directory (or create it if not present):
cd xml-to-json-frontend

# Install dependencies and create the React app:
npx create-react-app .

# Connect React App to Backend
Make sure your React app is fetching from the correct backend URL (e.g., http://localhost:8000/api/xmlToJson).

For local development, ensure CORS is enabled in FastAPI backend (see backend section).

(Optional) Add the following proxy to your package.json in frontend to simplify API requests:

"proxy": "http://localhost:8000"


# Start the development server:
npm start

## Deployment

You can deploy this API to any cloud environment supporting FastAPI (Render, Railway, Heroku, Vercel, etc.). Ensure the `/api/xmlToJson` endpoint is publicly accessible after deployment.
