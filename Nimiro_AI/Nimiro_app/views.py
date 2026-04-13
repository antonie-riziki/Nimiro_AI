from django.shortcuts import render, get_object_or_404, redirect
from google import genai
from google.genai import types
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import *
import africastalking
import requests
import os
import json
import sys



from dotenv import load_dotenv

load_dotenv()


YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")
PEXEL_API_KEY=os.getenv("PEXEL_API_KEY")


sys.path.insert(1, './Nimiro_app')



# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username="EMID",
    api_key=os.getenv("AT_API_KEY")
)

sms = africastalking.SMS


def get_gemini_response(prompt):

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=
            
                """
                
                You are Nimiro AI, a specialized agricultural assistant for Kenyan farmers. Your primary goal is to provide practical, location-specific guidance that helps farmers increase yields, reduce costs, and improve sustainability.

                🎯 Core Purpose

                Help Kenyan farmers:

                - Choose the right crops for their specific location
                - Optimize planting and harvesting times
                - Manage soil health and fertility
                - Control pests and diseases effectively
                - Access market information and pricing
                - Make informed decisions about inputs and practices

                You may provide global context when useful, but always prioritize relevance to Kenya when the question involves Kenyan agriculture.

                🗣 Tone & Style

                Your responses must be:

                - Conversational and easy to understand
                - Practical and actionable
                - Respectful of local farming knowledge
                - Encouraging and supportive
                - Clear and concise

                Avoid:

                - Overly technical jargon
                - Complex scientific explanations unless necessary
                - Generic advice that doesn’t consider Kenyan conditions
                - Discouraging or negative language

                🌍 Geographic Scope

                Primary focus:

                - Kenya
                - All agricultural zones (highlands, lowlands, coastal, arid/semi-arid)
                - Specific counties and regions when relevant

                Secondary scope:

                - East Africa (Uganda, Tanzania)
                - Relevant global best practices

                When giving global examples, clearly indicate:

                - Why it is relevant to Kenyan farmers
                - How it compares to local conditions

                📚 Knowledge Domains

                You should be able to assist with:

                - Crop selection based on soil type, rainfall, and market demand
                - Planting calendars and seasonal planning
                - Fertilizer and soil amendment recommendations
                - Pest and disease identification and management
                - Irrigation techniques suitable for Kenyan water availability
                - Harvesting and post-harvest handling
                - Market prices and value addition opportunities
                - Climate change adaptation strategies
                - Organic and sustainable farming practices

                🧠 Explanation Framework

                When answering:

                - Start with a short direct answer.
                - Provide practical guidance.
                - Explain why it matters in simple terms.
                - Suggest next steps or follow-up actions.

                Example structure:

                - Quick Answer
                - Why it matters for Kenyan farmers
                - Practical steps
                - Helpful tip

                🔎 When the User is Researching

                If a user asks about:

                - A specific crop → provide planting times, soil needs, market info.
                - A pest or disease → give identification, prevention, and treatment options.
                - Their location → tailor advice to their agro-ecological zone.
                - Market prices → provide current trends and where to find reliable data.

                If unsure:

                - Ask clarifying questions politely.
                - Suggest possible directions instead of saying “I don’t know.”

                🚫 Limitations & Boundaries

                Do not:
                - Give medical advice for humans
                - Provide financial or investment advice
                - Make guarantees about yields or profits
                - Claim real-time market data access

                If exact availability is unknown, say:

                “I don’t have real-time access to market data, but here’s where you can check…”

                🧩 Conversational Enhancements

                When appropriate:

                - Use relatable examples from Kenyan farming
                - Offer comparisons to similar crops or techniques
                - Encourage experimentation and learning

                Offer follow-up questions like:
                “What type of soil do you have?”
                “Which crops have you grown successfully before?”

                But avoid excessive questioning.

                ✨ Personality

                You are:

                - Knowledgeable about Kenyan agriculture
                - Practical and results-oriented
                - Supportive of smallholder farmers
                - Committed to sustainable practices

                Never sound arrogant or dismissive.
                Always prioritize actionable advice over theory.

                📌 Response Length Guidelines

                - Short questions → concise responses
                - Practical guidance → detailed but clear
                - Always prioritize clarity over length

                """,
            max_output_tokens= 1000,
            top_k= 2,
            top_p= 0.5,
            temperature= 0.9,
            # response_mime_type= 'application/json',
            # stop_sequences= ['\n'],
            seed=42,
        ),

    )
    
    return response.text



# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def auth_page(request):
    return render(request, 'auth.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')

def farming_guide(request):
    return render(request, 'farming_guide.html')

def market_intelligence(request):
    return render(request, 'market_intelligence.html')

def profile_page(request):
    return render(request, 'profile_page.html')

def landmap(request):
    return render(request, 'landmap.html')

def credit_score(request):
    return render(request, 'credit_score.html')

def analysis_page(request):
    return render(request, 'analysis.html')

def crop_calendar(request):
    return render(request, 'crop_calendar.html')

import random
PEXELS_URL = "https://api.pexels.com/videos/search"

REEL_QUERIES = [
    # General agriculture
    "farming",
    "agriculture",
    "modern farming",
    "smart farming",
    "precision agriculture",
    "digital agriculture",
    "sustainable farming",
    "organic farming",
    "regenerative agriculture",

    # African context (high priority)
    "african farming",
    "african agriculture",
    "kenyan farmers",
    "east africa farming",
    "smallholder farmers africa",
    "rural farming africa",
    "african agritech",
    "agritech africa",
    "farming in kenya",
    "nigeria agriculture",
    "uganda farming",
    "tanzania agriculture",

    # Farmers & activities
    "local farmers",
    "small scale farmers",
    "subsistence farming",
    "planting season",
    "harvesting crops",
    "farm work daily life",
    "tractor farming africa",

    # Crops & production
    "maize farming",
    "wheat farming",
    "rice farming africa",
    "horticulture farming",
    "vegetable farming",
    "fruit farming africa",
    "greenhouse farming",

    # Soil & inputs
    "soil testing",
    "soil health",
    "fertilizer application",
    "organic fertilizer",
    "compost farming",
    "soil nutrients",

    # Water & climate
    "irrigation systems",
    "drip irrigation africa",
    "climate smart agriculture",
    "climate change farming",
    "drought farming solutions",
    "rainfed agriculture",

    # Pest & crop management
    "pest control farming",
    "crop protection",
    "integrated pest management",
    "crop rotation",
    "weed control farming",

    # Technology & innovation (important for Nimiro AI context)
    "iot farming",
    "ai in agriculture",
    "smart sensors farming",
    "farm data analytics",
    "precision farming technology",
    "satellite farming data",
    "agriculture startups africa",
    "farm innovation africa",

    # Market & business
    "farmers market africa",
    "market prices crops",
    "selling farm produce",
    "agriculture supply chain",
    "post harvest handling",
    "farm to market africa",
    "agribusiness africa",

    # Finance & impact
    "farmer financing",
    "agriculture loans africa",
    "crop insurance africa",
    "financial inclusion farmers",
    "farmer success stories",
    "agriculture impact stories"
]


def reels(request):
    query = random.choice(REEL_QUERIES)

    headers = {
        "Authorization": PEXEL_API_KEY
    }

    params = {
        "query": query,
        "per_page": 20
    }

    response = requests.get(PEXELS_URL, headers=headers, params=params)

    if response.status_code != 200:
        return render(request, "reels.html", {"reels": []})


    data = response.json()

    reels = []

    for video in data.get("videos", []):
        reels.append({
            "title": "Farming",
            "summary": "Farming style footage",
            "video_url": video["video_files"][0]["link"],
            "creator": "Pexels",
            "likes": "—",
            "comments": "—",
            "shares": "—",
            "hashtags": ["Farming", "Agriculture"]
        })

    return render(request, "reels.html", {"reels": reels})


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({'response': bot_reply})
        else:
            return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)
