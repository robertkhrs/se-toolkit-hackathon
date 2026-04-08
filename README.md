# LinguaSim

An AI-powered roleplay ecosystem that adapts to user-defined scenarios and builds personalized vocabulary reviews based strictly on conversational mistakes.

## Demo

![LinguaSim Web App](/assets/web_app.png)
*LinguaSim Web Application interface with dynamic topic selection and mistake correction.*

![LinguaSim Telegram Bot](/assets/telegram_bot.png)
*LinguaSim Telegram Bot.*

## Product Context

* **End users:** Language learners, travelers, students, and professionals seeking realistic conversational practice and specific scenario simulations.
* **Problem that the product solves:** Traditional language applications lack contextual, unscripted dialogue practice. Furthermore, they do not provide smart, personalized tracking of actual grammatical and lexical mistakes made by the user in real-time.
* **Your solution:** A dual-client ecosystem (Web Application and Telegram Bot) powered by a large language model (Llama 3.3 70B). The AI acts as a roleplay partner in any user-defined scenario, intelligently extracts genuine mistakes, provides corrections, and synchronizes this data into a centralized database for cross-platform review.

## Features

**Implemented features:**
* Full-stack architecture with FastAPI backend and PostgreSQL database.
* Dual end-user clients: A responsive Web UI (HTML/JS/CSS) and a Telegram Bot (`aiogram`).
* Cross-platform synchronization: Both clients share the same database and user state.
* Dynamic Topic Injection: Users can define custom roleplay scenarios (e.g., "At the airport", "Job interview").
* Smart Error Tracking: Strict LLM prompting ensures only actual mistakes are extracted and saved (no random conversational vocabulary).
* Interactive Quiz: Scrollable modal in the Web App and dynamic list in the Telegram bot to review corrected mistakes.

**Not yet implemented features:**
* Voice message support (Speech-to-Text and Text-to-Speech integration).
* User authentication system (OAuth / JWT) for the Web Application.
* Spaced Repetition System (SRS) algorithm for the vocabulary quiz.

## Usage

**Using the Web Application:**
1. Open the deployed Web App URL in your browser.
2. Select your target language from the dropdown menu.
3. Enter a specific scenario in the Topic input field (e.g., "Ordering coffee in Milan").
4. Start chatting! The AI will respond in character.
5. If you make a mistake, read the correction block.
6. Click the "📝 Quiz" button to view your accumulated mistake history.

**Using the Telegram Bot:**
1. Send `/start` to the bot.
2. Use the "🌐 Change Language" and "💬 Change Topic" buttons to configure your session.
3. Chat with the bot as your roleplay partner.
4. Use the "🧠 Quiz" button to retrieve your saved mistakes.
5. Use the "💻 Web Version" button to quickly access the browser interface.

## Deployment

* **Target OS:** The VM should run on `Ubuntu 24.04`.
* **Required Software:** * Git
    * Docker
    * Docker Compose

**Step-by-step deployment instructions:**

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/robertkhrs/se-toolkit-hackathon.git](https://github.com/robertkhrs/se-toolkit-hackathon.git)
   cd se-toolkit-hackathon
   ```
2. **Set up environment variables:**

* Create a .env file in the root directory and populate it with your API keys:

```bash
GROQ_API_KEY=your_groq_api_key_here
BOT_TOKEN=your_telegram_bot_token_here
```
3. **Build and run the containers:**
* Use Docker Compose to build the images and start the services (Backend API, Telegram Bot, and PostgreSQL database) in detached mode:

```bash
docker compose up -d --build
```

4. **Verify deployment:**

* Access the Web App at ```http://<YOUR_VM_IP>:8000/```
* Access the API Documentation at ```http://<YOUR_VM_IP>:8000/docs```
* Message your Telegram bot to verify the connection.
