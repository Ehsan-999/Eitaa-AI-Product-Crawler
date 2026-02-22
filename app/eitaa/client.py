"""
کلاینت اتصال به API ایتا با استفاده از کتابخانه eitaa (eitaapykit)
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    from eitaa import Eitaa
    EITAA_AVAILABLE = True
except ImportError:
    EITAA_AVAILABLE = False
    print("[Warning] کتابخانه eitaa نصب نشده است. pip install eitaa")


class EitaaClient:
    """
    کلاینت برای اتصال به API ایتا با استفاده از eitaapykit
    
    برای استفاده:
    1. Token را از سایت https://eitaayar.ir دریافت کنید
    2. Token را در .env تنظیم کنید: EITAA_TOKEN=your_token
    """
    
    def __init__(self):
        """Initialize Eitaa client"""
        self.token = os.getenv("EITAA_TOKEN")
        self.client = None
        
        if EITAA_AVAILABLE and self.token and self.token != "your_eitaayar_token_here":
            try:
                self.client = Eitaa(self.token)
                print("[EitaaClient] Initialized with token")
            except Exception as e:
                print(f"[EitaaClient] Error initializing: {e}")
                self.client = None
        else:
            if not EITAA_AVAILABLE:
                print("[EitaaClient] Library not available, using mock data")
            elif not self.token or self.token == "your_eitaayar_token_here":
                print("[EitaaClient] Token not configured, using mock data")
    
    def search_channels(self, keyword: str, limit: int = 50) -> List[Dict]:
        """
        جستجوی کانال‌ها بر اساس کلمه کلیدی
        
        نکته: کتابخانه eitaa جستجوی مستقیم کانال ندارد
        اما می‌توان از get_trends برای پیدا کردن هشتگ‌های مرتبط استفاده کرد
        
        Args:
            keyword: کلمه کلیدی برای جستجو
            limit: حداکثر تعداد نتایج
            
        Returns:
            لیست کانال‌های پیدا شده
        """
        if not EITAA_AVAILABLE:
            return []
        
        try:
            # استفاده از trends برای پیدا کردن هشتگ‌های مرتبط
            trends = Eitaa.get_trends()
            
            # جستجو در trends برای پیدا کردن هشتگ‌های مرتبط
            channels = []
            for period in ["last_12_hours", "last_24_hours", "last_7_days"]:
                if period in trends:
                    for trend in trends[period]:
                        hashtag_name = trend.get("name", "").lower().replace("#", "")
                        if keyword.lower() in hashtag_name or hashtag_name in keyword.lower():
                            # ساخت channel_id از هشتگ
                            channels.append({
                                "channel_id": hashtag_name,
                                "name": trend.get("name", ""),
                                "members": 0,  # اطلاعات members در trends موجود نیست
                                "link": f"https://eitaa.com/{hashtag_name}",
                                "keyword": keyword,
                                "count": trend.get("count", "0"),
                            })
                            if len(channels) >= limit:
                                break
                if len(channels) >= limit:
                    break
            
            return channels[:limit]
            
        except Exception as e:
            print(f"[EitaaClient] Search error: {e}")
            return []
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict]:
        """
        فقط دریافت اطلاعات کانال از API (بدون token).
        اگر کانال معتبر نباشد None برمی‌گرداند.
        """
        if not EITAA_AVAILABLE:
            return None
        cid = (channel_id or "").strip().lstrip("@")
        if not cid or " " in cid or cid.startswith("http"):
            return None
        try:
            return Eitaa.get_info(cid)
        except Exception:
            return None

    def get_channel_preview(self, channel_id: str) -> Dict:
        """
        دریافت اطلاعات اولیه کانال (Bio و چند پست آخر).
        نیاز به token ندارد.
        """
        if not EITAA_AVAILABLE:
            return {
                "channel_id": channel_id,
                "bio": "",
                "recent_posts": [],
            }
        cid = (channel_id or "").strip().lstrip("@")
        if not cid or " " in cid:
            return {"channel_id": channel_id, "bio": "", "recent_posts": []}
        
        try:
            info = Eitaa.get_info(cid)
            messages = Eitaa.get_latest_messages(cid)
            
            # تبدیل به فرمت مورد نیاز
            recent_posts = []
            for msg in messages[:5]:  # فقط 5 پست آخر
                text = msg.get("text", "")
                if text:
                    recent_posts.append(text)
            
            return {
                "channel_id": cid,
                "bio": info.get("description", ""),
                "recent_posts": recent_posts,
                "name": info.get("name", ""),
                "users": info.get("users", "0"),
                "is_verified": info.get("is_verified", False),
            }
            
        except Exception as e:
            print(f"[EitaaClient] Get preview error for {cid}: {e}")
            return {"channel_id": cid, "bio": "", "recent_posts": []}
    
    def get_channel_posts(
        self, 
        channel_id: str, 
        limit: int = 100
    ) -> List[Dict]:
        """
        دریافت پست‌های یک کانال
        
        Args:
            channel_id: شناسه کانال (بدون @)
            limit: حداکثر تعداد پست
            
        Returns:
            لیست پست‌ها
        """
        if not EITAA_AVAILABLE:
            return []
        cid = (channel_id or "").strip().lstrip("@")
        if not cid or " " in cid:
            return []
        
        try:
            messages = Eitaa.get_latest_messages(cid)
            posts = []
            for msg in messages[:limit]:
                posts.append({
                    "post_id": str(msg.get("message_number", "")),
                    "text": msg.get("text", ""),
                    "images": [msg.get("image_link", "")] if msg.get("image_link") else [],
                    "views": msg.get("views", 0),
                    "date": msg.get("iso_time", ""),
                })
            
            return posts
            
        except Exception as e:
            print(f"[EitaaClient] Get posts error for {cid}: {e}")
            return []
    
    def get_message(self, channel_id: str, message_id: int) -> Optional[Dict]:
        """
        دریافت یک پست خاص از کانال
        
        Args:
            channel_id: شناسه کانال
            message_id: شماره پست
            
        Returns:
            اطلاعات پست
        """
        if not EITAA_AVAILABLE:
            return None
        
        try:
            message = Eitaa.get_message(channel_id, message_id)
            return message
        except Exception as e:
            print(f"[EitaaClient] Get message error: {e}")
            return None


# Singleton instance
_client: Optional[EitaaClient] = None


def get_client() -> EitaaClient:
    """Get or create Eitaa client instance"""
    global _client
    if _client is None:
        _client = EitaaClient()
    return _client
