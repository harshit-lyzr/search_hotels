import os

from fastapi import FastAPI, Query
from pydantic import BaseModel
import serpapi
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

app = FastAPI()

# Define the search_hotels function
def search_hotels(location: str, check_in_date: str, check_out_date: str, adults: str, currency: str, api_key: str):
    params = {
        "engine": "google_hotels",
        "q": location,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
        "gl": "us",  # Geolocation for the search
        "hl": "en",  # Language for the search results
        "api_key": api_key
    }

    search = serpapi.search(params)
    return search

# Create a Pydantic model for the query parameters
class HotelSearchParams(BaseModel):
    location: str
    check_in_date: str
    check_out_date: str
    adults: str
    currency: str = "INR"  # Default currency is INR

# Define a route to handle hotel searches
@app.post("/search_hotels")
def search_hotels_endpoint(params: HotelSearchParams):
    results = search_hotels(
        location=params.location,
        check_in_date=params.check_in_date,
        check_out_date=params.check_out_date,
        adults=params.adults,
        currency=params.currency,
        api_key=api_key
    )
    return results["properties"]
