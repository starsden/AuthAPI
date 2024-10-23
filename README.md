# FastAPI User Management Application

This is a simple user management application built with FastAPI. It allows users to sign up, log in, and view their profiles. The application uses JWT tokens for authentication and stores user data in a database.

 ## Features

- User registration (signup)
- User login with token-based authentication
- Profile viewing
- Basic error handling
- HTML templates for rendering responses

## Technologies Used

- FastAPI
- SQLAlchemy (for database interactions)
- Jinja2 (for HTML templating)
- OAuth2 (for secure token-based authentication)
- Python 3.x

## Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/starsden/AuthAPI.git
   cd AuthAPI
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   # On Windows use
  ```bash
  venv\Scripts\activate
  ```
4. Install the required packages:

   ```bash
   pip install fastapi[all] sqlalchemy jinja2
   ```

5. Initialize the database:

   Make sure to implement the `init_db()` function in your `models.py` to create the necessary tables.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

## API Endpoints

### Sign Up

- **POST** `/signup`
  
  **Form Data:**
  - `username`: str
  - `email`: str
  - `password`: str
  
  **Response:** Redirects to `/success` on successful signup.

### Login

- **POST** `/token`
  
  **Form Data:**
  - `username`: str
  - `password`: str
  
  **Response:** Redirects to `/profile?username=<username>` on successful login and sets a cookie with the access token.

### Profile

- **GET** `/profile?username=<username>`
  
  **Response:** Renders the profile page of the specified user.

### Success Page

- **GET** `/success`
  
  **Response:** Renders a success message after signup.

### Home Page

- **GET** `/`
  
  **Response:** Renders the main index page.

### Login Page

- **GET** `/login`
  
  **Response:** Renders the login page.

## Error Handling

Custom error handling can be implemented by uncommenting the exception handler in the code. This will allow rendering of custom error pages for specific HTTP status codes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
```

Feel free to modify any sections as needed, especially regarding installation instructions or any additional features you may want to highlight!
