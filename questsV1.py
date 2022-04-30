import logging
import sys
import time
import settings
import traceback
import requests
from web3 import Web3
from quests.professions import gardening
from quests.professions import minning
import quests.quest_v1 as quest_v1
from quests.utils import utils as quest_utils
import hero.hero as heroes
import dex.master_gardener

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

def calc_level_up_exp(level):
  return sum(map(lambda x: 1000 * int((x-1)/5) + 1000, range(level+1)))

def get_min_stamina(quest, hero_ids):
    if(len(hero_ids) == 0): return 0

    min_stamina=100
    for hero_id in hero_ids:
      stamina = quest.get_current_stamina(hero_id)
      if(stamina < min_stamina):
        min_stamina = stamina

    return min_stamina

if __name__ == "__main__":
  quest_type = sys.argv[1]
  quest_index = int(sys.argv[2])

  log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'

  logger = logging.getLogger("DFK-quest")
  logger.setLevel(logging.DEBUG)
  logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

  #rpc_server = 'https://api.harmony.one'
  rpc_server = 'https://rpc.cosmicuniverse.one'
  #rpc_server = 'https://harmony-0.gateway.pokt.network/v1/lb/61d4dc74431851003b635b82'
  logger.info("Using RPC server " + rpc_server)

  private_key = settings.PRIVATE_KEY  # set private key
  gas_price_gwei = 31
  tx_timeout = 60
  w3 = Web3(Web3.HTTPProvider(rpc_server))
  account_address = w3.eth.account.privateKeyToAccount(private_key).address

  questV1 = quest_v1.Quest(rpc_server, logger)

  pool_ids = [0, 15, 1, 2] # [JEWEL_ONE, JEWEL_AVAX, JEWEL_1ETH, JEWEL_1BTC]

#  dict_sell_hero = {
#    81878: 70,
#  }

  ##############################################################################
  # starting quest
  ##############################################################################
  while True:
    quest_hero_ids = getattr(settings, str.upper(quest_type)+'_HERO_IDS')[quest_index]
    quest_func = questV1.start_quest # gardening以外はこの関数なので初期値とする

    level = 1

    try:
      if(quest_type == 'jewel_mining'):
        arguments = (minning.JEWEL_QUEST_CONTRACT_ADDRESS, quest_hero_ids, 1,
          private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)

      elif(quest_type == 'gold_mining'):
        arguments = (minning.GOLD_QUEST_CONTRACT_ADDRESS, quest_hero_ids, 1,
          private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)

      elif(quest_type == 'gardening'):
        pool_id = pool_ids[quest_index] # See result of dex_example.py
        quest_hero_ids = [quest_hero_ids]
        quest_data = (pool_id, 0, 0, 0, 0, 0, '', '', ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS)

        quest_func = questV1.start_quest_with_data
        arguments = (gardening.QUEST_CONTRACT_ADDRESS, quest_data, quest_hero_ids, 1,
          private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)

      if(get_min_stamina(questV1, quest_hero_ids) >= 15):
        logger.info(*arguments)
        quest_func(*arguments)

        quest_info = quest_utils.human_readable_quest(questV1.get_hero_quest(quest_hero_ids[0]))

        logger.info(
            "Waiting " + str(quest_info['completeAtTime'] - time.time()) + " secs to complete quest " + str(quest_info))
        while time.time() < quest_info['completeAtTime']:
            time.sleep(2)


      quest_info = quest_utils.human_readable_quest(questV1.get_hero_quest(quest_hero_ids[0]))

      if quest_info is None:
        logger.info(f'quest did not start. quest_type: {quest_type} sleep 20 min')
        time.sleep(60*20)
        continue

    except KeyboardInterrupt:
      break
    except:
      traceback.print_exc()
      quest_info = quest_utils.human_readable_quest(questV1.get_hero_quest(quest_hero_ids[0]))
      time.sleep(10)

    ##############################################################################
    # completing quest
    ##############################################################################
    try:
      if quest_info is not None:
        sleep_time = quest_info['completeAtTime'] - time.time()
        logger.info(
            "Waiting " + str(sleep_time) + " secs to complete quest " + str(quest_info))

        if(sleep_time > 0):
          time.sleep(sleep_time + 30)

        tx_receipt = questV1.complete_quest(quest_hero_ids[0], private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)
        quest_result = questV1.parse_complete_quest_receipt(tx_receipt)

        # checking level up
        for i in quest_hero_ids:
          hero = heroes.get_hero(i, rpc_server)
          readable_hero = heroes.human_readable_hero(hero)

          if(readable_hero['state']['xp'] >= calc_level_up_exp(int(readable_hero['state']['level']))):
            requests.post(settings.DISCORD_URL, { 'content': f'hero {readable_hero["id"]} has enough xp for level up' })

        logger.info("Rewards: " + str(quest_result) + " sleep 1 hours.")
        time.sleep(60*60)
    except KeyboardInterrupt:
      break
    except:
      traceback.print_exc()
      time.sleep(10)
