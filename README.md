a production-ready REST API for managing a book catalog, designed to showcase my entire backend development skill set as of October 18, 2026. 

This is my first milestone project, built to apply modern architectural patterns, database migrations, and containerization practices in a real-world scenario

stack:
*language: python 3.14
*framework: FastAPI
*ORM & DataBase: SQLAlchemy 2.0 & PostgreSQL
*migrations: Alembic
*security: JWT authentication 
*deploy: docker, docker-compose

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/andrey-codeP/MyLibrary
   cd your-repo-name
   ```

2. **Spin up the containers (API & Database):**
   ```bash
   docker-compose up --build
   ```

3. **Access the API Documentation:**
   Once the containers are running, open your browser and navigate to:
   * Swagger UI: `http://localhost:8000/docs`
