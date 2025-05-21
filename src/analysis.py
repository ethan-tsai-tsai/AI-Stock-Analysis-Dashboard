import json
from src.config import client, MODEL_NAME

def analyze_with_llm(ticker, indicators_summary):
    # Update prompt asking for a detailed justification of technical analysis and recommendations
    analysis_prompt = (
        f"You are a Stock Trader specializing in Technical Analysis at a top financial institution. "
        f"Here is the summary of technical indicators for {ticker}:\n\n{indicators_summary}"
        f"Provide a detailed justification of your analysis, explaining what patterns, signals, and trends you observe. "
        f"Then, based analysis results, provide a recommendation from the following options: "
        f"'Strong Buy', 'Buy', 'Weak Buy', 'Hold', 'Weak Sell', 'Sell', or 'Strong Sell'. "
        f"Return your output as a JSON object with two keys: 'action' and 'justification'."
    )

    # Call the LLM with the image part and the analysis prompt
    contents = [
        {'role': 'user', 'content': analysis_prompt}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=contents,
    )

    try:
        result_text = response.choices[0].message.content
        print(result_text)
        json_start_index = result_text.index('{')
        json_end_index = result_text.rindex('}') + 1

        if json_start_index != -1 and json_end_index > json_start_index:
            json_str = result_text[json_start_index:json_end_index]
            result = json.loads(json_str)
        else:
            raise ValueError("No valid JSON found in the response.")
    except json.JSONDecodeError as e:
        result = {
            "action": "Error",
            "justification": f"JSON Parsing error: {e}. Raw response text: {response.choices[0].message.content}"
        }
    except ValueError as ve:
        result = {
            "action": "Error",
            "justification": f"Value Error: {ve}. Raw response text: {response.choices[0].message.content}"
        }
    except Exception as e:
        result = {
            "action": "Error",
            "justification": f"General Error: {e}. Raw response text: {response.choices[0].message.content}"
        }
    return result
