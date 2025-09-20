# APPROACH.md

## Overview

This document details the approach and design decisions taken for building a fullstack XML to JSON converter as required by the assignment. The project consists of a FastAPI backend with a custom XML parser (no XML libraries used), and a React frontend for user interaction.

---

## Objectives

- Implement an XML parser from scratch, fully in Python, without any parsing library.
- Expose parser functionality through a REST API endpoint: `/api/xmlToJson`.
- Design the system to correctly handle complex XML features (declaration, comments, attributes, nested elements, self-closing tags, entities, mixed content).
- Build an attractive React UI for file upload and JSON output.
- Ensure robust error handling, thorough testing, and cloud deployment readiness.

---

## XML Parser Approach

### Why Manual Parsing?

XML parsing libraries like `xml.etree.ElementTree` or `lxml` cannot be used per assignment rules. Therefore, the solution relies on string processing, regular expressions, and recursive parsing to manually interpret the XML structure.

### Parser Steps and Logic

1. **Remove XML Declaration & Comments**
    - Uses regular expressions to strip out the header (`<?xml ... ?>`) and comments (`<!-- ... -->`), as these are not structural content.

2. **Tokenization**
    - Splits the raw XML string into tokens (tags and text) using regex.
    - Each token is either a tag (`<tag>`, `</tag>`, or `<tag/>`) or text sitting between tags.

3. **Recursive Parsing**
    - Walks through tokens to build the XML tree structure.
    - For each opening tag, recursively parses its children until a closing tag or end.
    - Collects text content, handles mixed content, and manages sibling elements with the same tag name as arrays.

4. **Attribute and Entity Handling**
    - Attributes in tags are parsed via regex and stored under a special `"@attributes"` key in dictionaries.
    - Entity references (`&amp;`, `&lt;`, etc.) are replaced with actual characters via a helper function.

5. **Self-Closing Tags**
    - Detected and processed without expecting child nodes, but attributes are captured.

6. **Output**
    - The result is a nested Python dictionary mimicking the original XML structure.
    - This dictionary is directly JSON-serializable for output.

### Error Handling

- File validation (extension check).
- Exception handling to capture parsing errors and return descriptive error messages.

---

## API Design

- RESTful endpoint `/api/xmlToJson` (POST).
- Expects multipart file upload; does not require extra body content.
- Responds with JSON representation of the uploaded XML, or a relevant error message.

---

## Frontend Approach

- React app with a clean single-page UI.
- User uploads an XML file via a styled file input and button.
- On upload, React sends the file via `fetch` to the backend endpoint and displays returned JSON.
- Download option for JSON output.
- Error messages rendered for user guidance.
- Frontend designed for clarity and responsiveness; styling done using inline CSS and, optionally, UI libraries.

---

## Deployment

- Both frontend and backend are prepared for deployment on popular cloud services (e.g., Render, Railway, Vercel, Netlify, Heroku).
- CORS is configured on the backend to enable safe cross-origin requests.
- All setup, usage, and deployment instructions provided in `README.md`.

---

## Why This Design?

- Separation of concerns between parsing logic, API interface, and user interface.
- All parsing decisions made to handle ambiguity and edge cases in XML as per assignment requirements.
- Frontend and backend are loosely coupled for modular testing and deployment.

---

## Limitations

- No support for advanced XML features like namespaces or CDATA sections (these were outside assignment scope, but could be extended for real-world use).
- No external parsing libraries as per assignment constraints; performance and error handling are coded manually.

---

## Summary

This implementation achieves reliable XML parsing to JSON for most practical XML scenarios, following a completely manual approach. The result is a maintainable, extensible fullstack solution, thoroughly documented, and ready for assessment.
