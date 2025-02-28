import requests
import streamlit as st

def get_rent_estimate(address, bedrooms, bathrooms, square_footage):
    api_key = "246cd005b13d46728109a1ab3ac73bba"  # Ensure API key is a string
    url = "https://api.rentcast.io/v1/avm/rent/long-term"  # Updated endpoint
    headers = {"X-Api-Key": api_key}  # Corrected API key header
    
    params = {
        "address": address,
        "propertyType": "Apartment",
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "squareFootage": square_footage,  # Now using user input
        "compCount": 15
    }  # Proper query parameters
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 404:
            return "Error: The requested resource was not found. Check the address format."
        elif response.status_code == 401:
            return "Error: Unauthorized. Check your API key."
        elif response.status_code != 200:
            return f"HTTP error occurred: {response.status_code} - {response.text}"
        
        data = response.json()
        
        rent_value = data.get('rent', 'N/A')  # Ensure 'rent' key exists with a default value
        
        if isinstance(data, dict):
            return f"Estimated rent for {bedrooms} bed, {bathrooms} bath, {square_footage} sqft at {address}: ${rent_value} per month"
        else:
            return "No rental data found for this property."
    except requests.exceptions.Timeout:
        return "Error: The request timed out. Try again later."
    except requests.exceptions.RequestException as e:
        return f"Error fetching rental data: {str(e)}"

# Streamlit UI
st.title("Rental Estimate Tool")
st.write("Enter a property address to estimate rent.")

address = st.text_input("Property Address")
bedrooms = st.number_input("Number of Bedrooms", min_value=0, step=1)
bathrooms = st.number_input("Number of Bathrooms", min_value=0, step=1)
square_footage = st.number_input("Square Footage", min_value=100, step=50)  # New user input

if st.button("Get Rent Estimate"):
    if address and bedrooms and bathrooms and square_footage:
        estimate = get_rent_estimate(address, bedrooms, bathrooms, square_footage)
        st.write(estimate)
    else:
        st.error("Please fill in all fields.")

