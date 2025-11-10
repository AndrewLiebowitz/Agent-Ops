# This file (main.py) contains the Python code for the external tool.
# It's a simple Flask-based web server, wrapped by the functions-framework.

import functions_framework
import requests
from flask import jsonify

def get_mtg_card_info(card_name):
    """
    Retrieves key information for a Magic: The Gathering card from the public API.
    """
    base_url = "https://api.magicthegathering.io/v1/cards"
    params = {"name": card_name}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()

        if not data.get('cards'):
            return None

        card_data = data['cards'][0]

        info = {
            "name": card_data.get('name'),
            "mana_cost": card_data.get('manaCost'),
            "type": card_data.get('type'),
            "text": card_data.get('text'),
            "power": card_data.get('power'),
            "toughness": card_data.get('toughness'),
            "image_url": card_data.get('imageUrl')
        }
        return info

    except requests.exceptions.RequestException:
        return None
    except (KeyError, IndexError):
        return None

@functions_framework.http
def mtg_card_tool(request):
    """
    An HTTP Cloud Function that acts as a tool for a Vertex AI Agent.
    It expects a JSON payload with a "card_name" key and returns card data.
    """
    if request.method != 'POST':
        return jsonify({"error": "Invalid request method. Please use POST."}), 405

    if not request.is_json:
        return jsonify({"error": "Invalid content type. Please send a JSON payload."}), 415

    request_json = request.get_json(silent=True)

    if not request_json or "card_name" not in request_json:
        return jsonify({"error": "Missing 'card_name' in JSON payload."}), 400

    card_name = request_json["card_name"]
    card_data = get_mtg_card_info(card_name)

    if card_data:
        return jsonify(card_data), 200
    else:
        error_payload = {"error": f"Card '{card_name}' not found or API is unavailable."}
        return jsonify(error_payload), 404
