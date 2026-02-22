"""
Wrapper برای استفاده sync از کلاینت ایتا
"""

from typing import List, Dict, Optional
from app.eitaa.client import get_client


def get_channel_info(channel_id: str) -> Optional[Dict]:
    """دریافت اطلاعات یک کانال از API ایتا (بدون token)."""
    return get_client().get_channel_info(channel_id)


def search_channels(keyword: str, limit: int = 50) -> List[Dict]:
    """
    جستجوی کانال‌ها (sync wrapper)
    
    Args:
        keyword: کلمه کلیدی
        limit: حداکثر تعداد نتایج
        
    Returns:
        لیست کانال‌ها
    """
    client = get_client()
    return client.search_channels(keyword, limit)


def get_channel_preview(channel: Dict) -> Dict:
    """
    دریافت preview کانال (sync wrapper)
    
    Args:
        channel: Dict شامل channel_id
        
    Returns:
        Dict شامل bio و recent_posts
    """
    client = get_client()
    channel_id = channel.get("channel_id") or channel.get("id")
    
    # اگر channel_id شامل @ است، آن را حذف کن
    if channel_id and channel_id.startswith("@"):
        channel_id = channel_id[1:]
    
    return client.get_channel_preview(channel_id)


def get_channel_posts(channel: Dict, limit: int = 100) -> List[Dict]:
    """
    دریافت پست‌های کانال (sync wrapper)
    
    Args:
        channel: Dict شامل channel_id
        limit: حداکثر تعداد پست
        
    Returns:
        لیست پست‌ها
    """
    client = get_client()
    channel_id = channel.get("channel_id") or channel.get("id")
    
    # اگر channel_id شامل @ است، آن را حذف کن
    if channel_id and channel_id.startswith("@"):
        channel_id = channel_id[1:]
    
    return client.get_channel_posts(channel_id, limit)
