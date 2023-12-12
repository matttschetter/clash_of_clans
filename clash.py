import pandas as pd
import json, requests, urllib.parse
from datetime import datetime, timezone

# API Token & Player/Clan Tags
API_KEY = 'your_api_key_here'
player_tag = '#V8LJL8GG'
clan_tag = '#LG2JORVY'

# API Headers: Generally
headers = {
    'authorization': 'Bearer ' + API_KEY,
    'Accept': 'application/json'
}

# Function to encode URL
def urlEncode(tag):
    return urllib.parse.quote(tag)

# Standard Clash of Clans API Call function
def apiWithGetType(headers, api_url, get_type):
    request_response = requests.get(api_url, headers=headers)
    json_data = json.loads(request_response.text)
    if not get_type in json_data or len(json_data[get_type]) == 0:
        return []
    return pd.json_normalize(json_data, get_type)

def getClanWarLeagueRoundList(headers, league_group_tag):
    """
    Fetches a list of Clan War League rounds for a specific league group.

    Parameters:
    headers (dict): Headers to be used in the API request, including authorization.
    league_group_tag (str): Tag of the specific league group to fetch round details from.

    Returns:
    DataFrame: A DataFrame containing a list of Clan War League rounds.
    """
    # Encode the league group tag for URL
    league_group_tag_encoded = urlEncode(league_group_tag)

    # Construct the request URL for the Clan War League round list endpoint
    url = f'https://api.clashofclans.com/v1/clanwarleagues/wars/{league_group_tag_encoded}'

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return pd.json_normalize(json_data, 'rounds')
    else:
        print(f"Error: response status is {response.status_code}")
        print("Response body:", response.text)
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Example usage
league_group_tag = '#example_league_group_tag'  # Replace with actual league group tag
clan_war_league_round_list_df = getClanWarLeagueRoundList(headers, league_group_tag)
print(clan_war_league_round_list_df)

def getClanWarLeagueRound(headers, league_round_tag):
    """
    Fetches Clan War League round details.

    Parameters:
    headers (dict): Headers to be used in the API request, including authorization.
    league_round_tag (str): Tag of the specific league round.

    Returns:
    list: A list containing the war tags of the Clan War League round.
    """
    # Encode the league round tag for URL
    league_round_tag_encoded = urlEncode(league_round_tag)

    # Construct the request URL for the Clan War League round endpoint
    url = f'https://api.clashofclans.com/v1/clanwarleagues/wars/{league_round_tag_encoded}'

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        json_data = json.loads(response.text)
        # Extracting the war tags list
        if 'warTags' in json_data:
            return json_data['warTags']
        else:
            print("War tags not found in the response")
            return []
    else:
        print(f"Error: response status is {response.status_code}")
        print("Response body:", response.text)
        return []

# Example usage
league_round_tag = '#example_league_round_tag'  # Replace with actual league round tag
war_tags_list = getClanWarLeagueRound(headers, league_round_tag)
print(war_tags_list)
