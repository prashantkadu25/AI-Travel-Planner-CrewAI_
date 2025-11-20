import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM 
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI # Use this for Gemini LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI 

search_tool = SerperDevTool()

# Define AI Model
llm = LLM(
    provider="google", 
    # CRITICAL FIX: Switch to the stable, modern model name
    model="gemini-2.5-flash", 
    temperature=0.5,
    api_key=os.environ.get("GOOGLE_API_KEY") 
)

# --- Function to create AI Agents ---
# Define function to create agents
def create_agents(llm, destination, budget):
    
    # 1. DEFINE RESEARCHER
    researcher = Agent(
        role="Travel Researcher",
        goal=f"Find historical sites, public transport hotels, and real-time weather for {destination}.",
        backstory="You are an expert travel researcher, providing up-to-date information about history-focused trips.",
        verbose=True,
        memory=True,
        llm=llm,
        tools=[search_tool]
    )
    
    # 2. DEFINE BUDGET PLANNER
    budget_planner = Agent(
        role="Budget Planner",
        goal=f"Find budget flights, hotels, and activities within {budget} for {destination}.",
        backstory="You are a skilled budget analyst ensuring trips fit within financial constraints.",
        verbose=True,
        memory=True,
        llm=llm,
        tools=[search_tool]
    )

    # 3. DEFINE ITINERARY PLANNER
    itinerary_planner = Agent(
        role="Itinerary Planner",
        goal=f"Create a 3-day itinerary for {destination}, ensuring all historical sites are covered under {budget}.",
        backstory="You are an expert in trip planning, ensuring travelers get the best experience within their budget.",
        verbose=True,
        memory=True,
        llm=llm,
        tools=[search_tool]
    )

    # 4. FINAL RETURN (After all agents are defined)
    return researcher, budget_planner, itinerary_planner

# --- Streamlit UI ---
st.title("🌍 AI-Powered Travel Planner")
st.markdown("**Plan your perfect trip with AI-powered insights!**")

# --- Input Fields ---
destination = st.text_input("📍 Enter Destination (e.g., Hyderabad India):")
budget = st.text_input("💰 Enter Budget (e.g., 100000 INR):")

# --- Generate Travel Plan Button ---
if st.button("🎯 Generate Travel Plan"):
    if not destination or not budget:
        st.error("⚠️ Please enter both a destination and budget.")
    elif not os.environ.get("GOOGLE_API_KEY") or not os.environ.get("SERPER_API_KEY"):
        st.error("⚠️ API Keys not set. Please set GOOGLE_API_KEY and SERPER_API_KEY in your environment.")
    else:
        st.info("⏳ Generating your AI-powered travel plan... This may take a moment.")

        # Create AI Agents and Tasks
        researcher, budget_planner, itinerary_planner = create_agents(llm, destination, budget)

        research_task = Task(
            description=f"Find the best historical sites, weather forecast, and public transport hotels for {destination}.",
            expected_output="A list of top historical sites, a real-time weather update, and 3 hotel options near public transport.",
            agent=researcher
        )

        budget_task = Task(
            description=f"Find budget flights, hotel options, and daily costs for {destination} within {budget}.",
            expected_output=f"A full cost breakdown (flights, hotel, food, attractions) ensuring a {budget} budget is maintained.",
            agent=budget_planner
        )

        itinerary_task = Task(
            description=f"Plan a 3-day itinerary for {destination} under {budget}.",
            expected_output="A detailed 3-day plan, considering weather and budget constraints, with transport recommendations.",
            agent=itinerary_planner
        )

        # --- Create Crew ---
        crew = Crew(
            agents=[researcher, budget_planner, itinerary_planner],
            tasks=[research_task, budget_task, itinerary_task],
            process=Process.sequential
        )

        # --- Run AI Agents ---
        try:
            responses = crew.kickoff(inputs={'destination': destination, 'budget': budget})
            st.success("✅ Travel Plan Generated!")

            # 🛑 CRITICAL FIX: Display the final result directly
            st.subheader("🗺️ Final Travel Plan:")
            
            # Check if the output is a list/tuple (legacy format) or a single string (new format)
            if isinstance(responses, (list, tuple)) and len(responses) > 0:
                # If it's the old format, display the last (Itinerary Planner's) output
                st.markdown(responses[-1]) 
            else:
                # If it's a single string (the most common output now), display it directly
                st.markdown(responses)

        except Exception as e:
            st.error(f"An error occurred during Crew execution: {e}")

st.markdown("🌍 *Enjoy your AI-powered trip planning!* 🚀")