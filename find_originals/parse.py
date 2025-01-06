#!/usr/bin/env python3
"""
Find original shows from the GraphQL API from Anichart
"""
import sys
import json
import requests

def get_season(season, year):
    url = "https://graphql.anilist.co/"

    # Define your query and variables
    query = """
    query ($season: MediaSeason, $year: Int, $format: MediaFormat, $excludeFormat: MediaFormat, $status: MediaStatus, $minEpisodes: Int, $page: Int){
        Page(page: $page) {
            pageInfo {
                hasNextPage
                total
            }
            media(
                season: $season
                seasonYear: $year
                format: $format
                format_not: $excludeFormat
                status: $status
                episodes_greater: $minEpisodes
                isAdult: false
                type: ANIME
                sort: TITLE_ROMAJI
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
                    icon
                    color
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
    }
    """

    variables = {
        "season": season.upper(),
        "year": year,
        "format": "TV",
        "page": 1
    }

    # Convert the payload to JSON
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://anilist.co/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0"
        },
        data=json.dumps(payload)
    )

    return response

def parse_sources(response, filter=""):
    data = response.json()
    retval = {}
    shows = data["data"]["Page"]["media"]
    for show in shows:
        if not filter or filter.upper() in show["source"]:
            retval[show["title"]["romaji"]] = show["source"]
    
    return retval

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 parse.py <season> <year> [filter]")
        sys.exit(1)
    
    season = sys.argv[1]
    year = int(sys.argv[2])
    filter = sys.argv[3] if len(sys.argv) == 4 else ""
    response = get_season(season, year)
    sources = parse_sources(response, filter)
    print(season.upper(), " ", year)
    print("-------------------")
    # print(json.dumps(sources, indent=4))
    for item in sources.keys():
        print(" -", item)