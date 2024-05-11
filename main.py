import uvicorn
# main.py
# from starlette.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
# from websocket import manager


# from model.user import UserRouter
from model.students import StudentRouter
from model.administrator import AdministratorRouter
from model.account_approval import AccountApprovalRouter
from model.document_type import DocumentTypeRouter
from model.document_request import DocumentRequestRouter
from model.document_request_item import DocumentItemRouter
from model.document_transaction import DocumentTransactionRouter
from model.admin_approval import AdminApprovalRouter
from model.claiming_information import ClaimingInformationRouter
from model.courier_information import CourierInformationRouter
from model.user_transaction_history import UserTransactionHistoryRouter
from model.user_feedback import UserFeedbackRouter
from model.new_accounts import NewAccountsRouter
from model.add_student_user import AddStudentUserRouter
from model.add_admin_user import AddAdminUserRouter
from model.payment import PaymentsRouter
from model.auth import AuthRouter
from model.allusers import AllUsersRouter

# from fastapi.openapi.docs import get_swagger_ui_html    


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include CRUD routes from modules
app.include_router(AuthRouter, prefix="/api")
app.include_router(AllUsersRouter, prefix="/api")
app.include_router(DocumentRequestRouter, prefix="/api")
app.include_router(ClaimingInformationRouter, prefix="/api")
app.include_router(CourierInformationRouter, prefix="/api")

app.include_router(PaymentsRouter, prefix="/api")
app.include_router(NewAccountsRouter, prefix="/api")
app.include_router(AddStudentUserRouter, prefix="/api")
app.include_router(AddAdminUserRouter, prefix="/api")

# app.include_router(UserRouter, prefix="/api")
app.include_router(StudentRouter, prefix="/api")
app.include_router(AdministratorRouter, prefix="/api")
app.include_router(AccountApprovalRouter, prefix="/api")
app.include_router(DocumentTypeRouter, prefix="/api")

app.include_router(DocumentItemRouter, prefix="/api")
app.include_router(DocumentTransactionRouter, prefix="/api")
app.include_router(AdminApprovalRouter, prefix="/api")

app.include_router(UserTransactionHistoryRouter, prefix="/api")
app.include_router(UserFeedbackRouter, prefix="/api")




# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(data)
#     except Exception as e:
#         print(e)
#     finally:
#         await manager.disconnect(websocket) 

if __name__ == "__main__":
    uvicorn.run(app)