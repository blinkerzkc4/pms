from celery import shared_task
from websocket import WebSocket


@shared_task
def send_notification(websocket_url):
    ws = WebSocket()
    ws.connect(websocket_url)
    print("Connected:", ws.recv())
    ws.send("")
    print("Received:", ws.recv())
    ws.close()
