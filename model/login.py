from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector

router = APIRouter()

# MySQL connection configuration
db_config = {
    "host": "localhost",
    "user": "username",
    "password": "password",
    "database": "reqease"
}

# Model for user authentication
class UserLogin(BaseModel):
    email: str
    password: str

# Endpoint for user authentication
@router.post("/api/login")
def login(user_data: UserLogin):
    try:
        # Authenticate user (implement your authentication logic here)
        # Assuming authentication is successful, fetch user data including the role from the database
        user_data_with_role = fetch_user_with_role(user_data.email)
        
        if user_data_with_role:
            # Return user data along with the role
            return user_data_with_role
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Function to fetch user data including the role from the database
def fetch_user_with_role(email: str):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch user data including the role
    query = "SELECT u.*, a.role FROM user u LEFT JOIN administrator a ON u.user_id = a.user_id WHERE u.email = %s"
    cursor.execute(query, (email,))
    user_data_with_role = cursor.fetchone()

    # Close database connection
    cursor.close()
    conn.close()

    return user_data_with_role
