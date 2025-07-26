# Configure logging
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pdf_qa_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)