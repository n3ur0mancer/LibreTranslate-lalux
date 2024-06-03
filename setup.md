# Lalux-Translate Linux Setup

## Requirements
- Ubuntu
- Python & pip
- Virtual Environment (venv)

## Installation

1. **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Copy the .env File**
    Ensure you have the `.env` file in the root directory of your project. If not, copy it from the provided source.

    | Variable           | Description                                |
    |--------------------|--------------------------------------------|
    | `DB_HOST`          | The hostname of the database server        |
    | `DB_PORT`          | The port number the database server listens on |
    | `DB_NAME`          | The name of the database                   |
    | `DB_USER_READER`   | The username for the database reader       |
    | `DB_USER_SUPER`    | The username for the superuser             |
    | `DB_PASSWORD`      | The password for the database users        |


3. **Create and Activate Virtual Environment**
    ```bash
    python3.10 -m venv ll-translate
    source ll-translate/bin/activate
    ```

4. **Install psycopg2-binary**
    ```bash
    python -m pip install psycopg2-binary
    ```

5. **Install Requirements**
    ```bash
    cd <main_directory>
    pip install -r requirements.txt
    ```

6. **Start the Application**
    ```bash
    python3 main.py
    ```
    - The application should start on localhost port 5000.

## Troubleshooting

If you encounter a "module not found" error, follow these steps:

1. **Check in `ll-translate/lib64` Directory**
    - Verify if the module is present in `ll-translate/lib64`.

2. **Uninstall Package**
    - If the module is not present, it might be installed at the user level. Uninstall it:
        ```bash
        pip uninstall <PACKAGE>
        ```

3. **Re-install Package**
    - Re-install the package using the following syntax:
        ```bash
        python -m pip install <PACKAGE>
        ```

4. **Re-check Installation**
    - Confirm that the module is now present in the `lib64` directory.

## Postgres in Docker Container

1. **Install Docker**
    Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker.

2. **Start Docker Compose**
    ```bash
    docker-compose up
    ```

3. **Manage Docker Container**
    - To start the container:
        ```bash
        docker start lalux_translate
        ```
    - To check running containers:
        ```bash
        docker ps
        ```
    - To stop the container:
        ```bash
        docker stop CONTAINER_ID
        ```

4. **Create Translations Table**
    Run the provided SQL script to create the `translations` table in your PostgreSQL database.

5. **Import Data**
    Import your data into the `translations` table.

6. **Create Webapp User**
    Create a `webapp_user` with SELECT permissions for the `translations` table.

    ```sql
    CREATE USER webapp_user WITH PASSWORD 'password';
    GRANT SELECT ON translations TO webapp_user;
    ```

Following these steps will set up Lalux-Translate on your Ubuntu system, using a virtual environment for Python dependencies, and managing your Postgres database within a Docker container.
