from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
async def get():
    return HTMLResponse("""
        <html>
            <body>
                <h2>WebSockets</h2>
                <button onclick="connect()">Connect</button>
                <button onclick="sendMessage()">Send Message</button>
                <script>
                    let ws;
                    function connect() {
                        ws = new WebSocket("ws://localhost:8000/ws");
                        ws.onopen = function () {
                            console.log("Connected to WebSocket");
                        };
                        ws.onmessage = function (event) {
                            console.log("Received: " + event.data);
                        };
                        ws.onclose = function () {
                            console.log("Connection closed");
                        };
                    }
                    function sendMessage() {
                        ws.send("Hello from client");
                    }
                </script>
            </body>
        </html>"""
    )

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received: {data}")
        await websocket.send_text(f"Server received: {data}")