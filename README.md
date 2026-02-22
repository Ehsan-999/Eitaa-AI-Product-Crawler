# Eitaa AI Product Crawler

# خزنده هوشمند و موتور جستجوی محصولات ایتا

------------------------------------------------------------------------

## 🇬🇧 Overview

Eitaa AI Product Crawler is an AI-powered distributed crawling pipeline
designed to:

1.  Discover shop channels on Eitaa
2.  Validate them using AI
3.  Crawl and extract products
4.  Process data asynchronously using Redis Queue
5.  Provide semantic search using embeddings
6. Extracts structured product entities using LLM

------------------------------------------------------------------------

## 🇮🇷 معرفی پروژه

این پروژه یک پایپ‌لاین هوشمند مبتنی بر هوش مصنوعی است که:

1.  کانال‌های فروشگاهی ایتا را کشف می‌کند
2.  با استفاده از AI آن‌ها را اعتبارسنجی می‌کند
3.  محصولات را استخراج می‌کند
4.  با Redis Queue پردازش غیرهمزمان انجام می‌دهد
5.  موتور جستجوی معنایی مبتنی بر Embedding ارائه می‌دهد
6. و با استفاده از LLM اطلاعات ساخت‌ یافته محصول را استخراج می‌کند  

------------------------------------------------------------------------

## 🧠 Architecture \| معماری سیستم

    User Query
       ↓
    Discovery (Global Search)
       ↓
    AI Channel Validation
       ↓
    Crawler
       ↓
    Redis Queue
       ↓
    Worker (Embedding + DB)
       ↓
    Semantic Search Engine

------------------------------------------------------------------------

## ✨ Features \| ویژگی‌ها

- 🔍 **Discovery Phase**: تولید خودکار کلمات کلیدی و جستجوی کانال‌ها
- ✅ **Channel Validation**: اعتبارسنجی کانال‌ها با استفاده از AI
- 🕷️ **Crawling**: خزش و استخراج محصولات از کانال‌های تایید شده
- 📦 **Queue Management**: استفاده از Redis Queue برای پردازش غیرهمزمان
- 🔄 **Multi-Session**: پشتیبانی از چندین اکانت برای توزیع بار
- ⚡ **Rate Limiting**: مدیریت محدودیت‌های API
- 🔎 **Vector Search**: جستجوی هوشمند با استفاده از embeddings
- 🧠 **LLM-based Entity Extraction** استخراج موجودیت محصول با LLM

### 🔍 Discovery

-   Keyword-based channel discovery
-   Eitaa Global Search integration
-   Duplicate removal

### 🤖 AI Validation

-   Bio + recent posts analysis
-   AI-based shop classification

### 🕷 Crawling & Extraction

-   Product detection
-   Price extraction
-   Image extraction
-   Text extraction

### 📦 Distributed Queue

-   Redis-based job system
-   Asynchronous processing
-   Worker-based architecture

### 🔄 Multi-Session

-   Load distribution across accounts
-   Reduced risk of blocking

### ⚡ Rate Limiting & Backoff

-   Adaptive rate control
-   Failure recovery strategy

### 🔎 Semantic Search

-   OpenAI embeddings
-   Cosine similarity ranking
-   Natural language product search


### 🧠 AI-Based Product Entity Extraction
### 🧠 استخراج موجودیت محصول با LLM

Each product caption is processed using a Large Language Model (LLM) to extract structured entities:

هر کپشن محصول با استفاده از مدل زبانی پردازش شده و موجودیت‌های زیر استخراج می‌شود:

```json
{
  "sizes": ["38", "40", "42"],
  "colors": ["مشکی", "سفید"],
  "material": "مازراتی"
}
```

### ⚡ Rate Limiting & Anti-Blocking Strategy
### ⚡ استراتژی مدیریت محدودیت و جلوگیری از مسدودسازی


## 🇬🇧 Overview

Eitaa, like most messaging platforms, enforces request limits to ensure service stability and prevent abuse.
This system does not bypass platform protections, but instead implements a responsible and scalable request management strategy.
The goal is:

- Prevent account suspension
- Ensure long-term system stability
- Distribute load intelligently
- Respect platform rate policies

## 🇮🇷 معرفی

پلتفرم ایتا مانند سایر پیام‌رسان‌ها دارای محدودیت‌های نرخ درخواست (Rate Limit) است.
این سیستم مکانیزم‌های حفاظتی را دور نمی‌زند، بلکه با طراحی معماری صحیح از مسدود شدن اکانت‌ها جلوگیری می‌کند.
اهداف این بخش:

- جلوگیری از مسدود شدن اکانت‌ها
- پایداری بلندمدت سیستم
- توزیع هوشمند بار
- رعایت محدودیت‌های پلتفرم

### 🧩 Implemented Strategies | مکانیزم‌های پیاده‌سازی شده
## 1️⃣ Controlled Request Rate
## کنترل نرخ درخواست

- Requests are throttled using a configurable RateLimiter
- Example: 2 requests per second per session
- Prevents burst traffic

```python
rate_limiter = RateLimiter(rate_per_sec=2)
rate_limiter.wait()
```

## 2️⃣ Multi-Session Load Distribution
## توزیع بار بین چند اکانت

- Instead of sending all requests from a single account:
- Multiple authenticated sessions are used
- Requests are distributed across sessions
- Reduces pressure per account

```python
session_manager = SessionManager(["acc1", "acc2", "acc3"])
session = session_manager.get_session()
```

## 3️⃣ Exponential Backoff Strategy
## استراتژی Backoff تصاعدی

- When a request fails:
- System increases delay gradually
- Prevents rapid repeated failures
- Allows platform cooldown

```python
backoff.fail()
backoff.success()
```

Benefits:

- Avoids repeated triggering of rate limits
- Improves reliability

## 4️⃣ Queue-Based Processing Architecture
## معماری مبتنی بر صف

- Instead of direct database writes:
- Each product is queued in Redis
- Worker processes jobs asynchronously
- Crawling speed remains controlled

Advantages:

- Decoupled processing
- Stable throughput
- Scalable architecture

## 5️⃣ Failure Isolation
## جداسازی خطاها

- If one session fails, others continue
- Prevents total system downtime

## 🔐 Design Philosophy | فلسفه طراحی

This system follows a compliance-first approach:

- Controlled crawling
- Distributed load
- AI-assisted filtering
- Scalable infrastructure

## 📊 Production Considerations | ملاحظات محیط عملیاتی

For production-scale deployment:

- Dynamic rate adaptation
- Monitoring request success rate
- Automatic session rotation
- Alerting system for abnormal behavior

## 🏁 Conclusion | جمع‌بندی

The system is designed to operate sustainably within platform constraints by:

- Intelligent load distribution
- Rate control mechanisms
- Backoff strategies
- Queue-based processing

این سیستم با رعایت محدودیت‌های پلتفرم و طراحی معماری پایدار، از مسدود شدن اکانت‌ها جلوگیری کرده و امکان خزش بلندمدت را فراهم می‌کند.

------------------------------------------------------------------------

## 🛠 Tech Stack \| تکنولوژی‌ها

-   Python
-   PostgreSQL + pgvector
-   Redis
-   OpenAI API
-   RQ Worker
-   Docker

------------------------------------------------------------------------

## ⚙ Installation \| نصب و راه‌اندازی

### Requirements \| پیش‌نیازها

-   Python 3.8+
-   PostgreSQL with pgvector
-   Redis

### Install Dependencies

``` bash
pip install -r requirements.txt
```

### Run Infrastructure

``` bash
docker-compose up -d
```

### Environment Setup

``` bash
cp .env.example .env
```

Example:

``` env
DATABASE_URL=postgresql://user:pass@localhost:5432/eitaa
REDIS_HOST=localhost
REDIS_PORT=6379
OPENAI_API_KEY=your_openai_api_key_here
EITAA_TOKEN=your_eitaa_token_here
```

------------------------------------------------------------------------

## ▶ Running the Pipeline \| اجرای پایپ‌لاین

``` bash
python main.py discovery
python main.py validation
python main.py crawl
python -m app.worker.run_worker
```

------------------------------------------------------------------------

## 🔎 Semantic Search Example \| مثال جستجوی هوشمند

``` python
from app.search.semantic_search import search_products

results = search_products("کتونی سفید دخترانه", top_k=10)
```

------------------------------------------------------------------------

## ساختار پروژه

```
.
├── app/
│   ├── ai/              # ماژول‌های AI (embeddings)
│   ├── api/             # FastAPI endpoints
│   ├── crawler/         # خزش و استخراج محصولات
│   ├── db/              # مدل‌ها و اتصال دیتابیس
│   ├── discovery/       # فاز Discovery
│   ├── eitaa/           # کلاینت اتصال به API ایتا
│   ├── queue/           # مدیریت Redis Queue
│   ├── search/          # جستجوی هوشمند
│   ├── session/         # مدیریت session و rate limiting
│   ├── utils/           # توابع کمکی
│   ├── validation/      # اعتبارسنجی کانال‌ها
│   └── worker/          # Worker برای پردازش محصولات
├── data/                # فایل‌های داده (channels, products)
├── docker-compose.yml   # تنظیمات Docker
├── main.py              # اسکریپت اصلی Pipeline
├── .env.example         # env
└── requirements.txt     # Dependencies
```

------------------------------------------------------------------------

## 🔮 Future Improvements \| توسعه‌های آینده

-   Advanced channel scoring
-   Product category classification
-   Improved ranking algorithm
-   Monitoring & analytics dashboard

------------------------------------------------------------------------

## 🏁 Conclusion \| جمع‌بندی

This system provides a scalable and AI-powered infrastructure for
crawling and searching Eitaa marketplace products.

این سیستم یک زیرساخت مقیاس‌پذیر و مبتنی بر هوش مصنوعی برای خزش و جستجوی
محصولات ایتا فراهم می‌کند.
