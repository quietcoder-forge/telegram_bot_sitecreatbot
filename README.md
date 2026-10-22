# telegram_bot_sitecreatbot

# 🌐 SMIR FORGE — AI-Powered Website Generator

**SMIR FORGE** is a production-ready Telegram bot that empowers users to generate fully functional, responsive websites without writing a single line of code. By interpreting natural language inputs, the system leverages Generative AI to dynamically produce clean, production-ready HTML/CSS files and delivers them directly to the user.

## ✨ Core Features
*   **AI-Driven Generation:** Transforms a simple 3-step user prompt (Brand Name, Primary Color, Content) into a complete, standalone website.
*   **Smart Color Processing:** Intelligently distinguishes between the primary brand color and the background color to ensure optimal contrast and professional UI/UX.
*   **Dynamic Button Parsing:** Interprets custom syntax (e.g., `Button(Link, Text, Color)`) within user content and converts it into fully functional HTML `<a>` tags.
*   **Responsive & RTL Ready:** Outputs modern, mobile-first designs utilizing standard web fonts (Vazirmatn) with native Right-to-Left (RTL) support.
*   **Robust Error Handling:** Implements custom state management to prevent race conditions (e.g., multiple simultaneous generation requests) and gracefully handles API rate limits (HTTP 429) without crashing.
*   **Seamless Delivery:** Automatically converts AI text responses into downloadable `.html` documents within the Telegram interface.

## 🛠 Tech Stack
*   **Language:** Python 3.x
*   **Framework:** `aiogram` (Asynchronous Telegram Bot Framework)
*   **AI Engine:** Google Gemini API (LLM)
*   **Web Server:** `aiohttp` (for Webhook integration)
*   **Deployment:** Render (Cloud Hosting)

## 🏗 System Architecture & Design Decisions

The architecture of SMIR FORGE was designed with scalability, speed, and user experience in mind:

1.  **Webhook over Polling:** To ensure instant response times and prevent server resource exhaustion, the bot utilizes an asynchronous webhook architecture powered by `aiohttp`. This allows the bot to handle high traffic efficiently.
2.  **Finite State Machine (FSM):** Implemented `aiogram`'s FSM to strictly govern the user journey. This prevents users from bypassing steps and ensures the AI receives structured, valid inputs.
3.  **Advanced Prompt Engineering:** Designed a highly constrained System Prompt that forces the LLM to output only raw HTML, avoiding markdown wrappers or conversational filler. The prompt also enforces complex constraints (e.g., color hierarchy, button parsing).
4.  **Asynchronous Task Management:** Implemented safeguards to manage `async/await` flows correctly, ensuring that the bot remains responsive to other users while a website is being generated in the background.

## 🚀 Development Methodology & AI Integration

The true strength of this project lies in its development efficiency and modern engineering approach.

*   **Total Development Time:** **6 Hours**
*   **Strategic Division of Labor:** 
    This project was built using an **AI-Augmented Development** workflow. 
    *   **The Developer (Architect & QA):** Designed the entire system architecture, defined the FSM logic, engineered the complex AI system prompts, solved critical async state-management bugs (preventing multiple concurrent site generations), and handled cloud deployment.
    *   **The AI Assistant (Copilot & Boilerplate Generator):** Acted strictly as a supporting tool to accelerate development. AI was utilized solely for generating standard `aiohttp` webhook boilerplate, verifying forgotten syntax/imports, and refining the tone of UI text for a better user experience. 

By dividing tasks effectively, a production-ready SaaS-level Telegram bot was deployed from scratch to a live server in just 6 hours.

## 🌍 Localization Note
*The current user interface and the generated website outputs are in Persian (Farsi) to serve the domestic market. However, the underlying codebase, logic, and architecture are fully standardized (English variables/functions) and ready for international localization.*
