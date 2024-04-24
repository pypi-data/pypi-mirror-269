import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)
