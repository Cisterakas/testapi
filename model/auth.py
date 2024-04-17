from fastapi import APIRouter, Depends, HTTPException, Form
from passlib.context import CryptContext  # Password hashing

# Import your user model (replace with the actual path to your model)
from model.user import User  # Assuming your user model is in model.user

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/api/auth/login", response_model=dict)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db),
):
    # Fetch user by email
    user = await db.query(User).filter(User.email == email).first()

    # Validate user existence and password
    if not user or not pwd_context.verify(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Implement JWT authentication (replace with your token generation logic)
    # ...

    # Return the access token and some basic user information (without password)
    return {"access_token": token, "user_id": user.id, "email": user.email}

@router.post("/api/auth/register", response_model=dict)
async def register(
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db),
):
    # Validate email existence (optional)
    # existing_user = await db.query(User).filter(User.email == email).first()
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_password = pwd_context.hash(password.encode("utf-8"))

    # Create a new user
    new_user = User(email=email, password=hashed_password)
    await db.add(new_user)
    await db.commit()

    # Generate a JWT token (if using JWT authentication)
    # ...

    # Return the access token and basic user information (without password)
    return {"access_token": token, "user_id": new_user.id, "email": new_user.email}
