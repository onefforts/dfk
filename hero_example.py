import logging
import json
import sys
import requests
import settings
import hero.utils.utils as hero_utils
import hero.hero as heroes


if __name__ == "__main__":
    log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'

    logger = logging.getLogger("DFK-hero")
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

    rpc_server = 'https://api.harmony.one'
    logger.info("Using RPC server " + rpc_server)

    with open('hero/femaleFirstName.json', 'r') as f:
        female_first_names = hero_utils.parse_names(f.read())
    logger.info("Female hero first name loaded")

    with open('hero/maleFirstName.json', 'r') as f:
        male_first_names = hero_utils.parse_names(f.read())
    logger.info("Male hero first name loaded")

    with open('hero/lastName.json', 'r') as f:
        last_names = hero_utils.parse_names(f.read())
    logger.info("Hero last name loaded")

    # transfer(1, 'private key of the owner', 'next nonce of owner account', 'receiver address', 200, rpc_server, hero_abi_json, logger)

    for i in [2262, 3941, 6329, 7232, 7753, 10620, 65057, 73223, 81383, 81559, 81878, 84321, 92494, 96140, 96154, 98331]:
        logger.info("Processing hero #"+str(i))
        owner = heroes.get_owner(i, rpc_server)
        hero = heroes.get_hero(i, rpc_server)
        readable_hero = heroes.human_readable_hero(hero, male_first_names, female_first_names, last_names)
        logger.info(json.dumps(readable_hero, indent=4, sort_keys=False) + "\n Owned by " + owner)

        if(readable_hero['state']['xp'] >= (readable_hero['state']['level'] + 1) * 1000):
          requests.post(settings.DISCORD_URL, { 'content': f'hero {readable_hero["id"]} has enough xp for level up' })

