import os
import json
import google.generativeai as genai

### Setup Model ###

# Get gemini api key
os.environ["GEMINI_API_KEY"] = "AIzaSyA_nM-k1No4EnzQZedcmO_oaF3lrFYcRm8"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Setup model with low temp for deterministic results
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.2
    )
)

### Helper function(s) ###
def format_prompt(input_text):
    # function for creating prompt
    prompt = f"""
    The following input text, given after the **TEXT** marker, is from a drinks menu. Extract and structure the following in JSON format:
    - Short summary of the menu (is it a beer, a wine list, etc. | What are the key elements of the design?)
    - Array of products, for each:
        - Name
        - Description (if available)
        - Price (if available)
        - Brand (if recognised)
    - Breakdown of the branded percentage on the menu, for example Bacardi 40%, 10000 hours 20%, unbranded 40% (see brands list below).
    
    Recognised brand List:
        - Bacardi
        - 10000 hours
        - free reign
        - state of brewing
        - sierra nevada

    If the text is nonsensical, ignore that portion of the text.

    Here is an example of the structured output I am expecting:

    {{
        "menu_summary": "Beer menu with floral designs and a tropical theme",
        "products": [
            {{
                "name": "Sierra Nevada Pale Ale",
                "description": "A crisp, refreshing pale ale.",
                "price": "$13",
                "brand": "Sierra Nevada"
            }},
            {{
                "name": "State of Brewing Maguires Draught Stout",
                "price": "$10"
            }}
        ],
        "brand_percentages": {{
            "Sierra Nevada": 20,
            "State of Brewing": 40,
            "unbranded": 40
        }}
    }}

    **TEXT**:
    {input_text}
    """
    return prompt

### interaction with model ###
def query_model_to_json(input_text):
    # format prompt
    prompt = format_prompt(input_text)

    # get response from model
    response = model.generate_content(prompt)
    output = json.loads(response.text)

    return output

if __name__ == "__main__":
    # test API key configured correctly
    test_response = model.generate_content("Return a hello world JSON please")
    print(test_response)