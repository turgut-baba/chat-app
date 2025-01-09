from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.get("/interviewmq")
async def read_item(item_id: int):
    return {"item_id": item_id, "message": "Item fetched successfully"}

