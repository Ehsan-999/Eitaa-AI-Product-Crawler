# ماژول اتصال به API ایتا

این ماژول از کتابخانه `eitaa` (eitaapykit) برای اتصال به API ایتا استفاده می‌کند.

## نصب

```bash
pip install eitaa
```

## تنظیمات

در فایل `.env`:

```env
EITAA_TOKEN=your_token_from_eitaayar
```

Token را از سایت https://eitaayar.ir دریافت کنید.

## استفاده

### استفاده مستقیم از کلاینت

```python
from app.eitaa.client import EitaaClient

client = EitaaClient()

# جستجوی کانال‌ها (از trends)
channels = client.search_channels("خرید")

# دریافت preview کانال
preview = client.get_channel_preview("channel_id")

# دریافت پست‌ها
posts = client.get_channel_posts("channel_id", limit=100)
```

### استفاده از Sync Wrapper

```python
from app.eitaa.sync_wrapper import (
    search_channels,
    get_channel_preview,
    get_channel_posts
)

# جستجو
channels = search_channels("خرید")

# دریافت preview
preview = get_channel_preview({"channel_id": "channel_id"})

# دریافت پست‌ها
posts = get_channel_posts({"channel_id": "channel_id"}, limit=100)
```

## متدهای موجود

### بدون نیاز به Token

- `Eitaa.get_info(channel_id)` - دریافت اطلاعات کانال
- `Eitaa.get_latest_messages(channel_id)` - دریافت آخرین پیام‌ها
- `Eitaa.get_message(channel_id, message_id)` - دریافت یک پست خاص
- `Eitaa.get_trends()` - دریافت هشتگ‌های ترند

### نیاز به Token

- `Eitaa(token).send_message(...)` - ارسال پیام
- `Eitaa(token).send_file(...)` - ارسال فایل

## نکات مهم

1. **Channel ID**: باید بدون @ باشد (مثلاً `eitaa_faq` نه `@eitaa_faq`)
2. **جستجوی مستقیم وجود ندارد**: کتابخانه جستجوی مستقیم کانال ندارد، اما از trends استفاده می‌کند
3. **Fallback به Mock Data**: اگر token موجود نباشد یا خطا رخ دهد، از mock data استفاده می‌شود
