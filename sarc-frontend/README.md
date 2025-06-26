# SARC Frontend

This project is a React-based frontend for the SARC (Sistema de Alocação de Recursos Compartilhados) API. It allows users to manage buildings and rooms through a web interface.

## Prerequisites

Before running this frontend, ensure you have the following installed:
- Node.js (v18 or later recommended)
- npm (comes with Node.js)

The SARC backend API must be running and accessible. By default, this frontend is configured to connect to the API at `https://rh3rhyjrq2.execute-api.us-east-1.amazonaws.com/dev`.

## How to Execute the Frontend

1.  **Clone the repository (if you haven't already):**
    ```bash
    # If you are in the root of the main SARC project
    # No action needed if you only cloned the frontend part
    ```

2.  **Navigate to the frontend directory:**
    ```bash
    cd sarc-frontend
    ```

3.  **Install dependencies:**
    ```bash
    npm install
    ```

4.  **Run the development server:**
    ```bash
    npm run dev
    ```
    This will typically start the frontend application on `http://localhost:5173` (Vite's default) or `http://localhost:3000` if specified. Check your terminal output for the exact URL.

## Technologies Utilized

-   **React:** A JavaScript library for building user interfaces.
-   **Vite:** A fast build tool and development server for modern web projects.
-   **React Router DOM:** For handling routing and navigation within the single-page application.
-   **Axios:** A promise-based HTTP client for making API requests.
-   **JavaScript (ES6+):** The primary programming language.
-   **CSS:** For basic styling.

## Principal Functionalities Available

The frontend provides CRUD (Create, Read, Update, Delete) operations for the following entities:

### Buildings
-   **List Buildings:** View a list of all available buildings.
-   **Create Building:** Add a new building by providing its name.
-   **Edit Building:** Update the name of an existing building.
-   **Delete Building:** Remove a building from the system. (Note: Ensure rooms associated with a building are handled or re-assigned as per backend logic, though the frontend currently doesn't prevent deletion of buildings with rooms).

### Rooms
-   **List Rooms:** View a list of all rooms, including their name, associated building name, and capacity.
-   **Create Room:** Add a new room by providing its name, selecting its building from a list of existing buildings, and specifying its capacity.
-   **Edit Room:** Update the details (name, building, capacity) of an existing room.
-   **Delete Room:** Remove a room from the system.

## API Instance

This frontend is configured to work with the SARC API instance running at:
`https://rh3rhyjrq2.execute-api.us-east-1.amazonaws.com/dev`

If you are running a local instance of the API, you may need to update the `API_BASE_URL` in `sarc-frontend/src/services/api.js`.
