import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from google import genai
from google.genai import errors
from aiogram.types import BufferedInputFile


PROMPT_FA = """تو یک توسعه‌دهنده ارشد فرانت‌اند (Senior Front-End Developer) و یک طراح برتر UI/UX در سطح جهانی هستی. وظیفه تو دریافت سه متغیر ورودی به زبان فارسی و تبدیل آن‌ها به یک وب‌سایت تک‌صفحه‌ای (Single Page) فوق‌العاده مدرن، چشمنواز، حرفه‌ای و کاملاً واکنش‌گرا (Responsive) است.


### ورودی‌های کاربر (به زبان فارسی):
1. `اسم`: نام اصلی سایت (هویت برند).
2. `رنگ`: رنگ قالب و هویت بصری سایت (رنگ اکسنت).
3. `محتوا`: محتوای متنی سایت و دستورالعمل‌های ساخت دکمه.

---

### 📜 قوانین مطلق و حیاتی (این قوانین هرگز نباید نقض شوند):

#### ۱. خروجی صرفاً کد خام (Strict Raw Output)
- خروجی تو باید **فقط و فقط** کد خام و کامل HTML باشد.
- به هیچ عنوان از مارک‌داون (Markdown) مثل ` ```html ` استفاده نکن. (اگر این کار را بکنی سیستم کرش می‌کند).
- هیچ متن اضافه‌ای (حتی یک کلمه مثل "بفرمایید") قبل یا بعد از کد ننویس.
- خروجی باید دقیقاً با `<!DOCTYPE html>` شروع شده و با `</html>` تمام شود.
- تمام استایل‌های CSS باید داخل تگ `<style>` در همان فایل باشد.

#### ۲. موتور پردازش هوشمند دکمه‌ها (Button Parsing Engine)
در متغیر `محتوا`، کاربر ممکن است دستوراتی شبیه به `دکمه(باز کردن سایت apple.com)` یا `دکمه(رنگ قرمز؛ متن خرید)` بنویسد.
- **استخراج دقیق:** آدرس وب‌سایت (URL)، متن دکمه (Text) و رنگ دکمه (Color) را از داخل پرانتز بیرون بکش.
- **حذف از متن:** عبارت `دکمه(...)` باید **کاملاً از متن حذف شود** و به جای آن یک تگ `<a>` واقعی قرار بگیرد.
- **پردازش مستقل:** هر دستور `دکمه(...)` را جداگانه پردازش کن و برای هر کدام یک تگ `<a>` مستقل بساز.
- **افزودن پروتکل:** اگر آدرس مثل `apple.com` بود، حتماً `https://` را اضافه کن.
- **رفتار لینک:** حتماً از `target="_blank"` و `rel="noopener noreferrer"` استفاده کن.
- **کنتراست هوشمند:** متن روی دکمه‌ها باید همیشه کنتراست کافی داشته باشد. اگر روشنایی (luminance) رنگ دکمه بیشتر از ۵۰٪ بود، متن تیره (مثل مشکی یا خاکستری تیره) و اگر کمتر بود، متن روشن (سفید) انتخاب کن. از فرمول‌های ثابت استفاده نکن، فقط کنتراست را در نظر بگیر.

#### ۳. سیستم طراحی و رنگ (Design System & Colors)
- **قانون طلایی رنگ:** متغیر `رنگ` هرگز نباید به عنوان پس‌زمینه کل سایت استفاده شود. پس‌زمینه باید یک رنگ خنثی و لوکس (مثل `#f8fafc` یا `#ffffff`) باشد. از رنگ وارد شده فقط برای دکمه‌ها، لینک‌ها و جزئیات (Accents) استفاده کن.
- **تبدیل رنگ:** اگر مقدار متغیر `رنگ` به زبان طبیعی بود (مثل «صورتی»، «آبی نفتی»)، آن را به معادل HEX یا CSS معتبر تبدیل کن. اگر کد HEX یا مقدار معتبر CSS بود، دقیقاً همان را استفاده کن.
- **متغیرهای CSS:** حتماً از `:root` استفاده کن. **قانون سخت‌گیرانه:** هر CSS variable که تعریف می‌کنی باید حتماً حداقل یک بار در کد استفاده شده باشد. متغیر تعریف‌شده و استفاده‌نشده = کد آلوده.

#### ۴. تایپوگرافی و فونت (Typography)
- **فونت:** فونت Vazirmatn را دقیقاً از این CDN لود کن (این فونت روی Google Fonts نیست):
  `<link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">`
- در `font-family`، حتماً `Vazirmatn` اولین گزینه باشد. هرگز `system-ui` یا `-apple-system` را قبل از آن نگذار.
- **ممنوعیت:** روی متن‌های فارسی، استفاده از `letter-spacing` منفی یا غیرصفر کاملاً ممنوع است.

#### ۵. طراحی بصری و UI/UX (Modern & Sleek UI)
- **ساختار:** `<!DOCTYPE html><html lang="fa" dir="rtl">` با چیدمان Flexbox یا CSS Grid.
- **هدر (Header):** هدر جذاب با مقدار متغیر `اسم` (تگ `h1`، فونت درشت). هدر باید `sticky` باشد.
- **کارت محتوا:** متن‌ها داخل یک کارت با `border-radius` و `box-shadow` ملایم قرار بگیرند.
- **استایل دکمه‌ها:** دکمه‌های مدرن با افکت Hover. **قانون سخت‌گیرانه:** هرگز `transition: all` ننویس. فقط پراپرتی‌های واقعاً تغییرکننده را مشخص کن:
  `transition: transform 0.25s ease, box-shadow 0.25s ease, background-color 0.2s ease;`
  افکت Hover باید با `transform: translateY(-3px)` باشد.

#### ۶. واکنش‌گرایی (Responsive Design)
- استفاده از `@media (max-width: 768px)` برای موبایل. در موبایل، دکمه‌ها باید تمام عرض (100%) باشند.
- در موبایل، ارتفاع دکمه‌ها باید حداقل `44px` باشد (استاندارد Apple HIG و Google Material).

#### ۷. تمیزی کد (DRY - Don't Repeat Yourself)
- آیکون‌های SVG تکراری را یک بار با `<symbol>` و `<use>` تعریف کن.
- اگر چند دکمه سایه مشابه دارند، سایه را با `color-mix` از `--btn-color` بساز، نه سه بار تعریف دستی.
- برای دکمه‌های رنگی، hover را با `filter: brightness()` تغییر نده؛ با `color-mix` تیره‌تر کن.

#### ۸. دسترس‌پذیری و سئو (Accessibility & SEO)
- `:focus-visible` روی دکمه‌ها و لینک‌ها با `outline` رنگ برند.
- تگ `h1` فقط یک بار؛ بخش‌ها با `h2`؛ زیربخش‌ها با `h3`.
- هر `<img>` باید `alt` معنادار داشته باشد.
- هرگز `href="#"` روی عنصر غیرلینکی ننویس؛ برای لوگو از `href="/"` استفاده کن.
- `<meta name="description">` الزامی است.
- `<title>` باید مقدار متغیر `اسم` باشد یا با آن شروع شود.
- **کاهش حرکت (Reduced Motion):** برای کاربرانی که حساسیت حرکتی دارند، این کد CSS را به انتهای استایل‌ها اضافه کن:
  `@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }`

#### ۹. خودبازرسی قبل از خروجی (Self-Audit Checklist)
قبل از ارسال خروجی، این ۶ مورد را چک کن:
1. آیا `system-ui` قبل از `Vazirmatn` در `font-family` هست؟
2. آیا `letter-spacing` منفی روی متن فارسی هست؟
3. آیا `transition: all` وجود دارد؟
4. آیا آیکون‌های SVG تکراری در صفحه هست؟
5. آیا CSS variable تعریف‌شده ولی استفاده‌نشده هست؟
6. آیا `:focus-visible` روی دکمه‌ها هست؟

اگر پاسخ هر یک از موارد بالا «بله» بود، کد را بدون اطلاع‌رسانی اصلاح کن و دوباره خودبازرسی را اجرا کن تا همه «خیر» شوند. سپس خروجی بده.

---

### 🎯 دستور نهایی:
هر سه ورودی (اسم، رنگ، محتوا) را با دقت بخوان. سپس بدون نوشتن حتی یک کلمه توضیح اضافه، **فقط کد کامل HTML** را تولید کن که تمام قوانین بالا را رعایت کرده باشد. مستقیم با `<!DOCTYPE html>` شروع کن."""

guide_step1 = (
    "1️⃣ مرحله اول: نام سایت\n\n"
    "در این مرحله، نام اصلی سایت خود را وارد کنید. این نام با فونت درشت و زیبا در بالاترین بخش سایت (هدر) نمایش داده می‌شود.\n\n"
    "💡 مثال: فروشگاه من، کافه کهکشانی\n\n"
    "نام سایت خود را ارسال کنید:"
)
guide_step2 = (
    "2️⃣ مرحله دوم: رنگ قالب\n\n"
    "حالا رنگ اصلی سایت خود را مشخص کنید (می‌توانید نام رنگ یا کد رنگ بگویید).\n"
    "این رنگ برای دکمه‌ها و جزئیات سایت استفاده می‌شود، نه برای پس‌زمینه.\n\n"
    "💡 مثال: آبی نفتی، قرمز، یا #ec4899\n\n"
    "رنگ مورد نظر خود را ارسال کنید:"
)
guide_step3 =( 
    "📝 مرحله سوم: نوشتن محتوا (متن و دکمه‌ها)\n\n"
    "در این مرحله، متن اصلی سایتت رو بنویس. هرجا دوست داشتی یه دکمه باشه، از این فرمت استفاده کن:\n"
    "دکمه (لینک، متن، رنگ)\n\n"
    "نکته: لازم نیست هر سه رو بنویسی! هرچی ننویسی، هوش مصنوعی خودش بر اساس قالب سایتت انتخاب می‌کنه. فقط حتماً بینشون کاما (،) بذار.\n\n"
    "💡 ۳ مثال برای یادگیری سریع:\n\n"
    "۱. فقط لینک (ساده‌ترین حالت):\n"
    "دکمه (google.com)\n\n"
    "۲. لینک + متن دلخواه:\n"
    "دکمه (apple.com، متن: مشاهده محصولات اپل)\n\n"
    "۳. لینک + متن + رنگ دلخواه:\n"
    "دکمه (digikala.com، متن: خرید از دیجی‌کالا، رنگ: قرمز)\n\n"
    "📌 نمونه یک محتوای کامل:\n"
    "سلام به سایت من خوش آمدید!\n"
    "برای جستجو در اینترنت روی دکمه زیر کلیک کنید:\n"
    "دکمه (google.com، متن: جستجو، رنگ: آبی)"
)
sample_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="دانش و کیهان - نقش هوش مصنوعی در تحول اکتشافات فضایی، ماموریت‌های مریخ و مقالات علمی">
  <title>دانش و کیهان</title>
  <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" rel="stylesheet">
  <style>
    :root {
      --color-primary: #0f2b5c;
      --color-primary-hover: color-mix(in srgb, var(--color-primary) 80%, black);
      --color-bg: #f8fafc;
      --color-surface: #ffffff;
      --color-text-main: #1e293b;
      --color-text-muted: #475569;
      --color-border: #e2e8f0;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Vazirmatn', sans-serif;
      background-color: var(--color-bg);
      color: var(--color-text-main);
      line-height: 1.8;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .header {
      position: sticky;
      top: 0;
      z-index: 100;
      background-color: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--color-border);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .header-inner {
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand-logo {
      display: inline-flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: var(--color-primary);
    }

    .brand-logo svg {
      width: 32px;
      height: 32px;
      fill: currentColor;
    }

    .brand-title {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--color-primary);
    }

    .main-wrapper {
      flex: 1;
      max-width: 900px;
      width: 100%;
      margin: 2.5rem auto;
      padding: 0 1.5rem;
    }

    .content-card {
      background-color: var(--color-surface);
      border-radius: 16px;
      padding: 2.5rem;
      box-shadow: 0 10px 25px -5px rgba(15, 43, 92, 0.08), 0 8px 10px -6px rgba(15, 43, 92, 0.04);
      border: 1px solid var(--color-border);
    }

    .section-title {
      font-size: 1.25rem;
      color: var(--color-primary);
      margin-bottom: 1rem;
      font-weight: 700;
    }

    .lead-text {
      font-size: 1.125rem;
      color: var(--color-text-main);
      margin-bottom: 2rem;
      text-align: justify;
    }

    .action-group {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      margin-top: 1.5rem;
      margin-bottom: 2rem;
      padding: 1.5rem;
      background-color: #f1f5f9;
      border-radius: 12px;
      border-right: 4px solid var(--color-primary);
    }

    .action-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1.5rem;
      flex-wrap: wrap;
    }

    .action-label {
      color: var(--color-text-muted);
      font-size: 1rem;
      flex: 1;
      min-width: 240px;
    }

    .btn {
      --btn-color: var(--color-primary);
      --btn-text: #ffffff;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      padding: 0.75rem 1.5rem;
      min-height: 48px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.95rem;
      text-decoration: none;
      background-color: var(--btn-color);
      color: var(--btn-text);
      box-shadow: 0 4px 12px color-mix(in srgb, var(--btn-color) 35%, transparent);
      transition: transform 0.25s ease, box-shadow 0.25s ease, background-color 0.2s ease;
    }

    .btn svg {
      width: 18px;
      height: 18px;
      fill: currentColor;
    }

    .btn:hover {
      background-color: color-mix(in srgb, var(--btn-color) 82%, black);
      transform: translateY(-3px);
      box-shadow: 0 6px 16px color-mix(in srgb, var(--btn-color) 45%, transparent);
    }

    .btn:focus-visible {
      outline: 3px solid var(--color-primary);
      outline-offset: 3px;
    }

    .btn-blue {
      --btn-color: #2563eb;
      --btn-text: #ffffff;
    }

    .btn-dark {
      --btn-color: #111827;
      --btn-text: #ffffff;
    }

    .btn-green {
      --btn-color: #059669;
      --btn-text: #ffffff;
    }

    .concluding-text {
      font-size: 1.15rem;
      font-weight: 600;
      color: var(--color-primary);
      text-align: center;
      padding: 1.25rem;
      background-color: color-mix(in srgb, var(--color-primary) 6%, transparent);
      border-radius: 8px;
    }

    .footer {
      text-align: center;
      padding: 1.5rem;
      color: var(--color-text-muted);
      font-size: 0.875rem;
      border-top: 1px solid var(--color-border);
      background-color: var(--color-surface);
      margin-top: auto;
    }

    @media (max-width: 768px) {
      .content-card {
        padding: 1.5rem;
      }

      .action-item {
        flex-direction: column;
        align-items: stretch;
      }

      .btn {
        width: 100%;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      * {
        transition: none !important;
        animation: none !important;
      }
    }
  </style>
</head>
<body>

  <svg style="display: none;">
    <symbol id="icon-external" viewBox="0 0 24 24">
      <path d="M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3m-2 16H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7z"/>
    </symbol>
    <symbol id="icon-orbit" viewBox="0 0 24 24">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
    </symbol>
  </svg>

  <header class="header">
    <div class="header-inner">
      <a href="/" class="brand-logo" aria-label="صفحه اصلی دانش و کیهان">
        <svg aria-hidden="true"><use href="#icon-orbit"></use></svg>
        <h1 class="brand-title">دانش و کیهان</h1>
      </a>
    </div>
  </header>

  <main class="main-wrapper">
    <article class="content-card">
      <h2 class="section-title">هوش مصنوعی و افق‌های کیهانی</h2>
      <p class="lead-text">
        هوش مصنوعی (AI) در حال ایجاد یک انقلاب عظیم در حوزه اکتشافات فضایی است. الگوریتم‌های یادگیری ماشین امروزه به دانشمندان کمک می‌کنند تا حجم عظیمی از داده‌های ارسالی از تلسکوپ‌های فضایی و مریخ‌نوردها را با دقت و سرعتی باورنکردنی تحلیل کنند.
      </p>

      <div class="action-group">
        <div class="action-item">
          <span class="action-label">برای مطالعه بیشتر در مورد ماموریت‌های مریخ ناسا:</span>
          <a href="https://nasa.gov" target="_blank" rel="noopener noreferrer" class="btn btn-blue">
            <span>مشاهده ماموریت‌های ناسا</span>
            <svg aria-hidden="true"><use href="#icon-external"></use></svg>
          </a>
        </div>

        <div class="action-item">
          <span class="action-label">همچنین می‌توانید آخرین دستاوردهای شرکت اسپیس‌ایکس را در زمینه پرتاب موشک‌های هوشمند دنبال کنید:</span>
          <a href="https://spacex.com" target="_blank" rel="noopener noreferrer" class="btn btn-dark">
            <span>ورود به اسپیس‌ایکس</span>
            <svg aria-hidden="true"><use href="#icon-external"></use></svg>
          </a>
        </div>

        <div class="action-item">
          <span class="action-label">اگر به مقالات علمی معتبر در این زمینه علاقه دارید:</span>
          <a href="https://nature.com" target="_blank" rel="noopener noreferrer" class="btn btn-green">
            <span>مطالعه مقالات علمی</span>
            <svg aria-hidden="true"><use href="#icon-external"></use></svg>
          </a>
        </div>
      </div>

      <p class="concluding-text">
        آینده اکتشافات فضایی بدون هوش مصنوعی غیرقابل تصور است.
      </p>
    </article>
  </main>

  <footer class="footer">
    <p>&copy; تمام حقوق برای پایگاه دانش و کیهان محفوظ است.</p>
  </footer>

</body>
</html>"""
sample_name = "دانش و کیهان"
sample_color = "آبی نفتی"
sample_content = """هوش مصنوعی (AI) در حال ایجاد یک انقلاب عظیم در حوزه اکتشافات فضایی است. الگوریتم‌های یادگیری ماشین امروزه به دانشمندان کمک می‌کنند تا حجم عظیمی از داده‌های ارسالی از تلسکوپ‌های فضایی و مریخ‌نوردها را با دقت و سرعتی باورنکردنی تحلیل کنند.

برای مطالعه بیشتر در مورد ماموریت‌های مریخ ناسا:
دکمه (nasa.gov، متن: مشاهده ماموریت‌های ناسا، رنگ: آبی)

همچنین می‌توانید آخرین دستاوردهای شرکت اسپیس‌ایکس را در زمینه پرتاب موشک‌های هوشمند دنبال کنید:
دکمه (spacex.com، متن: ورود به اسپیس‌ایکس، رنگ: مشکی)

اگر به مقالات علمی معتبر در این زمینه علاقه دارید:
دکمه (nature.com، متن: مطالعه مقالات علمی، رنگ: سبز)

آینده اکتشافات فضایی بدون هوش مصنوعی غیرقابل تصور است."""

class register(StatesGroup):
    color = State()
    basecolor = State()
    name = State()
    websitetext = State()
    key = State()
    site = State()

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message : Message, state : FSMContext):
    await state.clear()
    
    builder = InlineKeyboardBuilder()
    buttom1 = InlineKeyboardButton(text="🔁شروع ساخت", callback_data="bott1")
    buttom2 = InlineKeyboardButton(text="دیدن نمونه کار✨", callback_data="bott2")
    builder.add(buttom1)
    builder.add(buttom2)
    builder.adjust(1)
    await message.answer(
    "برای شروع ساخت کافیه دکمه شروع و برای دیدن نمونه کار این ربات روی دیدن نمونه کار بزنید",
    reply_markup=builder.as_markup(),
)

@dp.callback_query(F.data == "bott1")
async def name(callback : CallbackQuery, state : FSMContext):
    await state.set_state(register.name)
    await callback.message.answer(guide_step1)
    await callback.answer()

@dp.message(F.text , StateFilter(register.name))
async def color(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(register.color)
    await message.answer(guide_step2)

@dp.message(F.text , StateFilter(register.color))
async def get_website_text(message : Message , state : FSMContext):
    await state.update_data(color = message.text)
    await state.set_state(register.websitetext)
    await message.answer(guide_step3)
     
@dp.message(F.text , StateFilter(register.websitetext))
async def ai_connect(message : Message , state : FSMContext):
    await state.update_data(websitetext = message.text)
    await message.answer("حالا صبر کن و منتظر پاسخ هوش مصنوعی باش ممکنه تا 5 دقیقه هم طول بکشه!⌛")
    data = await state.get_data()
    await state.clear()
    client = genai.Client(api_key=os.getenv("AI_TOKEN"))
    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"اسم سایت : {data['name']} رنگ سایت : {data['color']} محتوای سایت : {data['websitetext']}",
            config={"system_instruction": PROMPT_FA}
        )
    except errors.APIError as f:
        if f.code == 429:
            await message.answer("سهمیه هوش مصنوعی به اتمام رسیده ❌")
        else:
            await message.answer("خطای ناشناخته هنگام ساخت")
            await message.answer(f"error code : {f.code} ")
            print(f"err message : {f.message} err status : {f.status}")
        return


    
    builder2 = InlineKeyboardBuilder()
    buttom1 = InlineKeyboardButton(text="شروع ساخت دوباره", callback_data="bott1")
    buttom2 = InlineKeyboardButton(text="دیدن نمونه کار", callback_data="bott2")
    builder2.add(buttom1)
    builder2.add(buttom2)
    builder2.adjust(1)




    html_code = response.text

    

    document = BufferedInputFile(
        html_code.encode('utf-8'),
        filename="site.html"
    )
    await message.answer_document(
        document=document,
        caption="سایت ساخته شد ! برای مشاهده روی فایل کلیک کن  \n برای ساخت دوباره روی دیکمه زیر ضربه بزن",
        reply_markup=builder2.as_markup()

    )
    


@dp.callback_query(F.data == "bott2")
async def send_sample(callback : CallbackQuery):

    await callback.message.answer("👇 به عنوان نمونه، اطلاعات زیر رو به هوش مصنوعی دادیم:")
    await callback.message.answer(f"نام سایت: {sample_name}\nرنگ سایت: {sample_color}")
    await callback.message.answer(f"و محتوای اصلی سایت:\n{sample_content}")
    
    
    document = BufferedInputFile(
        sample_html.encode('utf-8'),
        filename="sample.html" 
    )

    
    await callback.message.answer_document(
        document=document,
        caption="فایل نمونه ارسال شد. برای مشاهده روی فایل سایت کلیک کنید."
    )

    await callback.answer()



async def on_startup(bot: Bot):
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        await bot.set_webhook(f"{render_url}/webhook")

def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp.startup.register(on_startup)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    port = int(os.getenv("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
