# 🌐 SMIR FORGE — AI-Powered Website Generator

SMIR FORGE is a fully functional Telegram bot that empowers users to generate complete, responsive websites without writing a single line of code. By interpreting natural language inputs, the system leverages Generative AI to dynamically produce clean HTML/CSS files and delivers them directly to the user.

## ✨ Core Features
*   **AI-Driven Generation:** Transforms a simple 3-step user prompt (Brand Name, Primary Color, Content) into a complete, standalone website.
*   **Smart Color Processing:** Intelligently distinguishes between the primary brand color and the background color to ensure optimal contrast and professional UI/UX.
*   **Dynamic Button Parsing:** Interprets custom syntax (e.g., `Button(Link, Text, Color)`) within user content and converts it into fully functional HTML `<a>` tags.
*   **Responsive & RTL Ready:** Outputs modern, mobile-first designs utilizing standard web fonts (Vazirmatn) with native Right-to-Left (RTL) support.
*   **Robust Error Handling:** Implements custom state management to prevent race conditions (e.g., multiple simultaneous generation requests) and gracefully handles API rate limits (HTTP 429) without crashing.
*   **Seamless Delivery:** Automatically converts AI text responses into downloadable `.html` documents within the Telegram interface.

## 🛠 Tech Stack
*   **Language:** Python 3.x
*   **Framework:** aiogram (Asynchronous Telegram Bot Framework)
*   **AI Engine:** Google Gemini API (LLM)
*   **Web Server:** aiohttp (for Webhook integration)
*   **Deployment:** Render (Cloud Hosting)

## 🏗 System Architecture & Design Decisions

*   **Asynchronous Webhook Architecture:** I chose a webhook approach over polling to ensure instant response times and prevent server resource exhaustion. *Note: The initial boilerplate for the `aiohttp` webhook was scaffolded by AI, as I am still deepening my understanding of this specific architecture. However, the integration, deployment, and debugging were handled manually.*
*   **Finite State Machine (FSM):** Implemented aiogram's FSM to strictly govern the user journey. This prevents users from bypassing steps and ensures the AI receives structured, valid inputs.
*   **Advanced Prompt Engineering:** Designed a highly constrained System Prompt that forces the LLM to output only raw HTML. *This was a collaborative process: I directed the AI on what constraints to apply (color hierarchy, button parsing, no markdown), and AI helped draft and refine the syntax.*
*   **Asynchronous Task Management:** Solved critical race conditions where rapid user inputs caused multiple concurrent generation requests, ensuring the bot remains responsive while generating sites in the background.

## 🚀 Development Methodology & AI Integration

The true strength of this project lies in its **AI-Augmented Development** workflow. I acted as the Lead Architect and directed the AI to act as an accelerator, not a replacement.

*   **Total Development Time:** 6 Hours (from zero to a live, deployed bot).
*   **My Role (The Developer):** I designed the entire system architecture, defined the business logic and FSM flow, handled the complex state management and bug fixing (such as preventing the bot from freezing during AI generation), managed deployment on Render, and directed the overall project vision.
*   **AI's Role (The Accelerator):** AI was used heavily to speed up development. It generated the complex webhook boilerplate (which I then integrated), assisted in drafting and refining the long system prompts based on my strict requirements, helped verify forgotten syntax/imports, and polished UI texts. 

*By dividing tasks effectively, a SaaS-level Telegram bot was deployed from scratch to a live server in just 6 hours. This project is also a continuous learning journey — I've been learning `aiogram` for only a month, and this project has been the ultimate hands-on training ground.*

## 🌍 Localization Note
The current user interface and the generated website outputs are in Persian (Farsi) to serve the domestic market. However, the underlying codebase, logic, and architecture are fully standardized (English variables/functions) and ready for international localization.
