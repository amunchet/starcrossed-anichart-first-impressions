#!/usr/bin/env python3
"""
Parses for Anichart -> Star Crossed First Impressions Format
"""
import requests
import json

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

response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    # Process the response data as needed
    print(data)
    with open("output.json", "w") as f:
        json.dump(data, f)
else:
    print("Request failed with status code:", response.status_code)