# 🌐 SMIR FORGE — AI-Powered Website Generator

SMIR FORGE is an experimental Telegram bot that generates complete, responsive websites based on user inputs. It leverages the Google Gemini API to write HTML/CSS code dynamically and delivers it directly to the user's chat. 

*Note: This project is a hands-on learning journey into `aiogram` and AI integration, built within the first month of my Python bot development experience.*

## ✨ Features
*   **AI Website Generation:** Transforms a simple 3-step prompt (Brand Name, Primary Color, Content) into a complete, standalone HTML file.
*   **Smart Color Processing:** Instructs the AI to distinguish between the primary brand color and the background to ensure readability.
*   **Custom Button Syntax:** Users can write `Button(Link, Text, Color)` in their content, and the AI converts it into actual HTML `<a>` tags.
*   **Responsive & RTL Ready:** Generates mobile-first designs with native Right-to-Left (RTL) support and Vazirmatn font.
*   **Basic Error Handling:** Prevents the bot from crashing when hitting Gemini API rate limits (HTTP 429) and displays a user-friendly message.
*   **Asynchronous Execution:** Utilizes async/await to ensure the bot can handle multiple users while an AI request is processing in the background.

## 🛠 Tech Stack
*   **Language:** Python 3.x
*   **Framework:** `aiogram` 3.x (Asynchronous Telegram Bot Framework)
*   **AI Engine:** Google Gemini API (`google-genai`)
*   **Web Server:** `aiohttp` (for Webhook integration)
*   **Deployment:** Render

## 🏗 Architecture & Design Decisions
*   **Webhook over Polling:** To ensure fast response times and prevent server resource exhaustion, the bot uses an `aiohttp` webhook server. *(The initial boilerplate for this specific architecture was scaffolded by AI, and I am actively learning the underlying mechanics).*
*   **Finite State Machine (FSM):** Uses `aiogram`'s FSM to strictly guide the user through the 3-step form, preventing users from skipping steps or sending invalid inputs.
*   **Highly Constrained Prompts:** The AI is restricted via system prompts to output *only* raw HTML, avoiding markdown wrappers (` ```html `) and conversational text, ensuring the output is directly usable.

## ⚠️ Known Limitations & Technical Debt
This is an ongoing project, and the following limitations are acknowledged:
*   **Security:** The webhook endpoint currently lacks a secret token validation, and tokens are loaded via environment variables (working, but needs hardening for public scale).
*   **Code Structure:** The project currently lives in a single file (`main.py`). It will be refactored into modular routers (`handlers/`, `services/`) as the codebase grows.
*   **Testing:** There are currently no automated unit tests. Testing is done manually via the Telegram interface.
*   **AI Rate Limits:** The bot relies on the free tier of Gemini API, which is strictly limited (e.g., 5 RPM, 20 RPD). The bot will stop generating sites if the quota is exhausted.
*   **Webhook Error Handling:** Lacks exponential backoff for failed webhook retries.

## 🚀 Getting Started (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/quietcoder-forge/telegram_bot_sitecreatbot.git
   cd telegram_bot_sitecreatbot
