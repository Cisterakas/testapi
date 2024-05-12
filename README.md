# BACKEND of the ReqEase : Registrar Document Request Suite

Welcome to the Registrar Document Request Suite! We are your one-stop online solution for all your school document needs. Whether you're looking for transcripts, enrollment verification, or any other official records, we've got you covered. 

## Authors

- Lead @Joshua Cister
- Support Lead @Juvenile Christen Bajo
- Member @Yukihiro Gamale
- Member @Christian Jade Plaza

## FastAPI Project Setup

This README outlines the steps to set up and run a FastAPI project along with necessary dependencies.

**Prerequisites**

Before you begin, ensure you have the following installed on your system:

- Anaconda or Miniconda
- Python 3.9 (optional if already installed via Anaconda)

## Running Tests and Setup Instructions

Clone this repository to your local machine:

```bash
git clone <repository_url> 
```

Navigate to the project directory:

```bash
cd <project_directory> 
```

Create a new Conda environment with Python 3.9:

```bash
conda create --name your_env_name python=3.9 
```

Activate the newly created Conda environment:

```bash
conda activate your_env_name 
```

Install required Python packages:

```bash
pip install fastapi uvicorn mysql-connector-python 
```

(If bcrypt is not already installed, run the following command:)

```bash
pip install bcrypt 
```

Start the FastAPI server:

```bash
uvicorn main:app --reload 
```

## Usage

- To access the FastAPI project, open your web browser and navigate to http://localhost:8000.
- Add "/docs" to open the FastAPI - Swagger UI

## Additional Notes
If you have previously opened the project and need to restart the server, follow these steps:

Navigate to the project directory:

```bash
cd <project_directory>
```

Activate the Conda environment:

```bash
conda activate your_env_name
```

Start the FastAPI server:

```bash
uvicorn main:app –reload
```

## Backend Tip

Remember to start the backend server if you want to open it in localhost using uvicorn main:app --reload. If you don't want to use localhost, you can deploy it to your preferred hosting service like Vercel.

That's it! You're all set to run tests with FastAPI and work with the backend.
