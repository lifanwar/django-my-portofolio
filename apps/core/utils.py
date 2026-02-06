# apps/core/utils.py

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_notification(name, email, message):
    """
    Send contact form notification via Telegram Bot API
    Returns True if successful, False otherwise
    """
    # Kalau credentials kosong, langsung skip
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        
        notification_text = (
            f"🔔 <b>New Contact Form Submission</b>\n\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Email:</b> {email}\n"
            f"<b>Message:</b>\n{message[:500]}{'...' if len(message) > 500 else ''}\n\n"
            f"<i>Check Django admin for full details</i>"
        )
        
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': notification_text,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        
        logger.info(f"Telegram notification sent: {email}")
        return True
        
    except Exception as e:
        logger.error(f"Telegram error: {str(e)}")
        return False
