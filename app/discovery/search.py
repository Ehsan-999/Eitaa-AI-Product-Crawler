import os
import random
from app.eitaa.sync_wrapper import search_channels as eitaa_search_channels, get_channel_info


def _channels_from_ids(channel_ids: str):
    """از لیست آیدی کانال‌ها (با کاما) لیست کانال با اطلاعات واقعی از API می‌سازد."""
    ids = [x.strip().lstrip("@") for x in channel_ids.split(",") if x.strip()]
    channels = []
    for cid in ids:
        if not cid or " " in cid:
            continue
        info = get_channel_info(cid)
        if info:
            channels.append({
                "channel_id": cid,
                "name": info.get("name", cid),
                "members": 0,
                "link": f"https://eitaa.com/{cid}",
                "keyword": "channel_list",
            })
    return channels


def search_channels(keyword: str):
    """
    جستجوی کانال‌ها در ایتا.
    اگر EITAA_CHANNEL_IDS در .env باشد، از همان کانال‌های واقعی استفاده می‌شود.
    """
    channel_ids = os.getenv("EITAA_CHANNEL_IDS", "").strip()
    if channel_ids:
        chs = _channels_from_ids(channel_ids)
        if chs:
            print(f"[Search] Using {len(chs)} channels from EITAA_CHANNEL_IDS")
            return chs
    
    token = os.getenv("EITAA_TOKEN")
    if token and token != "your_eitaayar_token_here":
        try:
            print(f"[Search] Using Eitaa API (trends) for keyword: {keyword}")
            channels = eitaa_search_channels(keyword, limit=50)
            if channels:
                print(f"[Search] Found {len(channels)} from API")
                return channels
        except Exception as e:
            print(f"[Search] API error: {e}, falling back to mock data")
    
    print(f"[Search] Using mock data for keyword: {keyword}")
    fake_channels = []
    for i in range(random.randint(2, 5)):
        fake_channels.append({
            "channel_id": f"{keyword}_{i}",
            "name": f"کانال {keyword} {i}",
            "members": random.randint(100, 50000),
            "link": f"https://eitaa.com/{keyword}_{i}",
            "keyword": keyword,
        })
    return fake_channels
