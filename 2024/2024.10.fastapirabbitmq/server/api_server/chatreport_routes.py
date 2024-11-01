from __future__ import annotations

from fastapi import APIRouter, Request
from server.api_server.chatreport import *


chatreport_router = APIRouter(prefix = "/copilot/app/chatreport", tags = ["智能事件录入"])


chatreport_router.post("/chat",
                 summary = "对话录入,追加式")(hello)