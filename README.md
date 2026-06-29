Project Title :-
AI_ROUTE_PLANNER

Introduction :-
AI Route Planner is a multi-agent application that generates intelligent travel recommendations using routing, traffic, and weather information. It uses LangGraph to coordinate specialized agents, LangSmith for monitoring, and Streamlit for the user interface.

Features :-
	• Source and destination input 
	• Current location support 
	• Multiple route generation 
	• AI route recommendation 
	• Live traffic analysis 
	• Weather prediction 
	• Interactive map 
	• Markdown travel report 
    • LangSmith monitoring

Technologies :-
	• Python 
	• LangGraph 
	• LangChain 
	• Groq Llama 3.3 
	• Streamlit 
	• Folium 
	• TomTom Routing API 
	• TomTom Traffic API 
	• TomTom Geocoding API 
	• OpenWeather API 
    • LangSmith

WorkFlow :- 

	     START
		   │
		   ▼
	    Planner agent
		   │
		   ▼
	    Geocode agent
		   │
		   ▼
	    Route agent    
	        |  
      ───────────────────
     │                   │
     ▼                   ▼         
 Traffic agent        Weather agent
        ▼                ▼   
        ───────────────────          
                │
                ▼
           Decision agent
                │
                ▼
           Report agent
                │
                ▼
	  Markdown Travel Report
                │
                ▼
	 Interactive Folium Map
                |
	            ▼  
               END

Architecture :- 

                            AI Route Planner

                                   User
                                    │
                                    ▼
                            Streamlit Frontend      
                            Source • Destination    
                                    │
                                    ▼
                             LangGraph Engine         
                                    │
                                    ▼
                                Planner Agent               
                            Extract Source & Dest        
                                    │
                                    ▼
                                Geocode Agent      
                            Convert → Coordinates 
                                    │
                                    ▼
                               Route Agent       
                             TomTom Routing      
                               │        │
                    ┌──────────┘        └──────────┐
                    ▼                              ▼
        
           Traffic Agent                      Weather Agent    
          TomTom Traffic                     OpenWeather API  
                   └──────────────┬───────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │      Decision Agent     │
                     │     Groq LLM Analysis   │
                     │ • Best Route            │
                     │ • Traffic Impact        │
                     │ • Weather Impact        │
                     │ • Departure Suggestion  │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │Report Generator         │
                     │Professional Markdown    │
                     │Travel Report            │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │Final Travel Report       │
                     │+ Interactive Map         │
                     └──────────────────────────┘




Installation :-

```bash
git clone https://github.com/USERNAME/AI_ROUTE_PLANNER.git

cd AI_ROUTE_PLANNER

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```


API Keys :-

GOOGLE_MAPS_API_KEY=AIz...
OPENWEATHER_API_KEY=0203...
TOMTOM_API_KEY=2XX...
GROQ_API_KEY=gsk_AT...
LANGCHAIN_API_KEY=lsv2...



How to Run :-

```bash
streamlit run app.py
```

