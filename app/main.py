import uuid
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.v1.endpoints import user # Importing routes/endpoints
from app.core.config import settings  # Import settings
from app.models.user import User  # Import the User model to create the table
from app.db.session import Base, engine


           

# Initialize FastAPI 
Base.metadata.create_all(bind=engine)
app = FastAPI(
     title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.ENVIRONMENT == "development"  # Enable debug mode if in development

)

# websocket_list = []

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
    
#     # Add the new websocket connection to the list
#     websocket_list.append(websocket)
#     print(websocket_list)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(data)
#             # Send the received message to all connected WebSockets except the sender
#             for web in websocket_list:
#                 if web != websocket:
#                     print(data)
#                     await web.send_text(f"Message from another client: {data}")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         # Remove the websocket connection when it disconnects
#         websocket_list.remove(websocket)
websocket_list = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Generate a unique ID for the new WebSocket connection
    user_id = str(uuid.uuid4())
    websocket_list[user_id] = websocket
    print(f"Connected: {user_id}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {user_id}: {data}")

            # Expecting data in the format "recipient_id:message"
            try:
                recipient_id, message = data.split(":", 1)
                recipient_id = recipient_id.strip()
                message = message.strip()

                # Send the received message to the specified recipient if they are connected
                if recipient_id in websocket_list:
                    await websocket_list[recipient_id].send_text(f"Message from {user_id}: {message}")
                else:
                    await websocket.send_text(f"User ID {recipient_id} is not connected.")
            except ValueError:
                await websocket.send_text("Invalid message format. Use 'recipient_id:message'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the websocket connection when it disconnects
        print(f"Disconnected: {user_id}")
        del websocket_list[user_id]

# Sample HTML client for testing
@app.get("/")
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Chat</title>
        <style>
            body { font-family: Arial, sans-serif; }
            #messages { width: 300px; height: 200px; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <textarea id="messages" cols="30" rows="10" readonly></textarea><br>
        <input type="text" id="recipient" placeholder="Recipient ID" autocomplete="off"/>
        <input type="text" id="input" autocomplete="off" placeholder="Type a message..."/><button id="send">Send</button>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            const messages = document.getElementById("messages");
            const input = document.getElementById("input");
            const recipient = document.getElementById("recipient");
            const sendButton = document.getElementById("send");

            ws.onmessage = function(event) {
                messages.value += event.data + '\\n';  // Display received message
                messages.scrollTop = messages.scrollHeight; // Scroll to the bottom
            };

            sendButton.onclick = function() {
                const message = input.value;
                const recipientId = recipient.value;
                if (message && recipientId) {
                    ws.send(`${recipientId}: ${message}`);  // Send message in the format "recipient_id:message"
                    input.value = '';
                    recipient.value = '';  // Clear recipient input
                }
            };

            input.addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    sendButton.click();
                }
            });
        </script>
    </body>
</html>
    """)

# CORS configuration (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your security needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])

# Health Check Route
@app.get("/health-check")
async def health_check():
    return {"status": "healthy"}

# You can add other application-level configurations here

if __name__ == "__main__":
    import uvicorn
    # This allows you to run the FastAPI server via `python main.py`
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
