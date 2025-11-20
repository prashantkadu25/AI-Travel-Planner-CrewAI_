# 🌍 AI-Powered Travel Planner (CrewAI & Gemini)

This project showcases a multi-agent system built using CrewAI, Streamlit, and the Gemini API to automatically research, budget, and plan a 3-day travel itinerary for any destination within a user-defined financial constraint.

## ⚙️ Project Overview

The application is built around three specialized AI agents that execute tasks sequentially:

1.  **Travel Researcher:** Finds historical sites, real-time weather, and hotel options.
2.  **Budget Planner:** Calculates a detailed cost breakdown (flights, hotel, food, attractions) based on the user's budget.
3.  **Itinerary Planner:** Creates a final, optimized 3-day schedule and recommends transport.

## 🚀 Getting Started

### Prerequisites

To run this application, you need to set up API keys for the AI model and the search tool.

1.  **Python 3.10+**
2.  **Gemini API Key:** Get your key from Google AI Studio.
3.  **Serper API Key:** Get your key from the Serper website.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/prashantkadu25/AI-Travel-Planner-CrewAI_.git](https://github.com/prashantkadu25/AI-Travel-Planner-CrewAI_.git)
    cd AI-Travel-Planner-CrewAI_
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # (Note: This includes crewai, streamlit, langchain-google-genai, litellm, etc.)
    ```

### Running the App

1.  **Set Environment Variables** (Required for the application to authenticate):

    In your **PowerShell** terminal, run:
    ```powershell
    $env:GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    $env:SERPER_API_KEY="YOUR_SERPER_API_KEY"
    ```

2.  **Launch the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser.

---
