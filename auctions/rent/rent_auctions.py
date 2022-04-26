import requests

AUCTIONS_OPEN_GRAPHQL_QUERY = """
                        query {
                          assistingAuctions(skip: %d, first: %d, orderBy: startingPrice, orderDirection: asc, where: {open: true}) {
                            id
                            seller {
                                name
                            }
                            tokenId {
                              id
                              owner {
                                owner
                              }
                              statGenes
                              generation
                              rarity
                              mainClass
                              subClass
                              summons
                              maxSummons
                              summonerId {
                                id
                              }
                              assistantId {
                                id
                              }
                            }
                            startingPrice
                            endingPrice
                            startedAt
                            duration
                            winner {
                              id
                              name
                            }
                            open

                          }

                        }
                        """


def get_open_auctions(graphql_address, skip=0, count=1000):

    r = requests.post(graphql_address, json={'query': AUCTIONS_OPEN_GRAPHQL_QUERY % (skip, count)})
    if r.status_code != 200:
        raise Exception("HTTP error " + str(r.status_code) + ": " + r.text)
    data = r.json()
    return data['data']['assistingAuctions']


def api_get_open_auctions(hero_ids=[]):

    r = requests.post("https://us-central1-defi-kingdoms-api.cloudfunctions.net/query_heroes", data='{"limit":100,"params":[{"field":"assistingprice","operator":">=","value":1000000000000000000},{"field":"id","operator":"in","value":[%s]}],"offset":0,"order":{"orderBy":"staminafullat","orderDir":"desc"}}' % ','.join(map(str, hero_ids)), headers={'Content-Type': 'application/json'})
    if r.status_code != 200:
        raise Exception("HTTP error " + str(r.status_code) + ": " + r.text)
    data = r.json()
    return data

