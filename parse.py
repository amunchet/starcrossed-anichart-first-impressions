#!/usr/bin/env python3
"""
Parses for Anichart -> Star Crossed First Impressions Format
    - With love from ChatGPT
"""
import requests
import json
import collections
import calendar
import sys

from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

url = "https://graphql.anilist.co/"
headers = {
    "Referer": "https://anichart.net/",
    "Content-Type": "application/json"
}
payload = {
    "query": """query (
	$season: MediaSeason,
	$year: Int,
	$format: MediaFormat,
	$excludeFormat: MediaFormat,
	$status: MediaStatus,
	$minEpisodes: Int,
	$page: Int,
){
	Page(page: $page) {
		pageInfo {
			hasNextPage
			total
		}
		media(
			season: $season
			seasonYear: $year
			format: $format,
			format_not: $excludeFormat,
			status: $status,
			episodes_greater: $minEpisodes,
			isAdult: false,
			type: ANIME,
			sort: TITLE_ROMAJI,
		) {
			
id
idMal
title {
	romaji
	native
	english
}
startDate {
	year
	month
	day
}
endDate {
	year
	month
	day
}
status
season
format
genres
synonyms
duration
popularity
episodes
source(version: 2)
countryOfOrigin
hashtag
averageScore
siteUrl
description
bannerImage
isAdult
coverImage {
	extraLarge
	color
}
trailer {
	id
	site
	thumbnail
}
externalLinks {
	site
	url
}
rankings {
	rank
	type
	season
	allTime
}
studios(isMain: true) {
	nodes {
		id
		name
		siteUrl
	}
}
relations {
	edges {
		relationType(version: 2)
		node {
			id
			title {
				romaji
				native
				english
			}
			siteUrl
		}
	}
}

airingSchedule(
	notYetAired: true
	perPage: 2
) {
	nodes {
		episode
		airingAt
	}
}

		}
	}
}""",
    "variables": {
        "season": "SUMMER",
        "year": 2023,
        "format": "TV",
        "page": 1
    }
}

author_block = [
    {'color': 'ff9900', 'html': '<span style="color: #ff9900;"><b>Lenlo:</b></span>', 'name': 'Lenlo'},
    {'color': '4b93ff', 'html': '<span style="color: #4b93ff;"><b>Amun:</b></span>', 'name': 'Amun'},
    {'color': '008000', 'html': '<span style="color: #008000;"><b>Mario:</b></span>', 'name': 'Mario'},
    {'color': 'ff0000', 'html': '<span style="color: #ff0000;"><b>Aidan:</b></span>', 'name': 'Aidan'},
    {'color': '800080', 'html': '<span style="color: #800080;"><b>Helghast:</b></span>', 'name': 'Helghast'},
    {'color': '8b0000', 'html': '<span style="color: #8b0000;"><b>Armitage:</b></span>', 'name': 'Armitage'},
    {'color': '0000ff', 'html': '<span style="color: #0000ff;"><b>Wooper:</b></span>', 'name': 'Wooper'}
]

env = Environment(loader=FileSystemLoader('.'), autoescape=True)  

# Load the template
template = env.get_template('output.html')  

def get_last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day
    
def convert_to_datetime(date_dict):
    year = date_dict.get('year', 0)
    month = date_dict.get('month', 1)
    day = date_dict.get('day', 1)
    
    if day is None:
        day = get_last_day_of_month(year, month)

    # Create a datetime object with the provided values
    date = datetime(year, month, day)

    return date
    
def main(season, year, override_file=""):
    """
    Main function to generate the output html
    """
    payload["variables"]["season"] = season.upper()
    payload["variables"]["year"] = year
    
    if override_file == "":
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
        else:
            print(response.text)
            raise Exception(f"Request failed with status code:{response.status_code}")
        
    else:
        with open(override_file) as f:
            data = json.load(f)
            
    
    days = collections.defaultdict(list)
    
    
    media = data["data"]["Page"]["media"]
    
    # Step 1: Organize by Start Date
    for (idx,show) in enumerate(media):
        try:
            startDate = convert_to_datetime(show["startDate"])
            days[startDate].append({
                "title" : show["title"]["romaji"],
                "synopsis" : show["description"].split("<br")[0],
                
            })
        except Exception:
            print("Had an exception in this item:", show)
    
    
    days = sorted(days.items(), key=lambda x: x[0])
    
    output = template.render(days=days, author_block=author_block)
    
    with open("render.html", "w") as f:
        f.write(output)
       
    print("Done")
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter [season] [year] to generate.  The file will be render.html")
    else:
        main(season=sys.argv[1], year=sys.argv[2])