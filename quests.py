import logging
import sys
import time
import settings
import traceback
import requests
from web3 import Web3
from quest import foraging
from quest import fishing
from quest import gardening
from quest import minning
from quest.quest import Quest
from quest.utils import utils as quest_utils
import hero.hero as heroes
import dex.master_gardener

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

if __name__ == "__main__":
  quest_type = sys.argv[1]

  log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'

  logger = logging.getLogger("DFK-quest")
  logger.setLevel(logging.DEBUG)
  logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

  rpc_server = 'https://api.harmony.one'
  #rpc_server = 'https://harmony-0.gateway.pokt.network/v1/lb/61d4dc74431851003b635b82'
  logger.info("Using RPC server " + rpc_server)

  private_key = settings.PRIVATE_KEY  # set private key
  gas_price_gwei = 31
  tx_timeout = 60
  w3 = Web3(Web3.HTTPProvider(rpc_server))
  account_address = w3.eth.account.privateKeyToAccount(private_key).address

  quest = Quest(rpc_server, logger)

  forager_hero_ids = [3941, 73223, 81383]
  fisher_hero_ids = [2262, 6329, 92494, 96140, 98331]
  miner_hero_ids = [7232, 96154, 81878, 10620]
  gardener_hero_ids = [7753, 65057, 81559, 84321, 106392, 106408]

  pool_ids = [0, 15, 1, 2, 3, 4] # [JEWEL_ONE, JEWEL_AVAX, JEWEL_1ETH, JEWEL_1BTC]

  ##############################################################################
  # starting quest
  ##############################################################################
  while True:
    quest_hero_ids = []

    try:
      if(quest_type == 'foraging'):
        quest_hero_ids = forager_hero_ids
        quest_func = quest.start_quest
        arguments = (foraging.QUEST_CONTRACT_ADDRESS, forager_hero_ids, 3, private_key,
          w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)

      elif(quest_type == 'fishing'):
        quest_hero_ids = fisher_hero_ids
        quest_func = quest.start_quest
        arguments = (fishing.QUEST_CONTRACT_ADDRESS, fisher_hero_ids, 3, private_key,
          w3.eth.getTransactionCount(account_address),
          gas_price_gwei, tx_timeout)

      elif(quest_type == 'gardening'):
        index = int(sys.argv[2]) # Gardeningでのみ使用
        pool_id = pool_ids[index] # See result of dex_example.py
        quest_hero_ids = [gardener_hero_ids[index]]
        quest_data = (pool_id, 0, 0, 0, 0, 0, '', '', ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS)

        quest_func = quest.start_quest_with_data
        arguments = (gardening.QUEST_CONTRACT_ADDRESS, quest_data, quest_hero_ids, 1,
          private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)

      elif(quest_type == 'minning'):
        quest_hero_ids = miner_hero_ids
        quest_func = quest.start_quest
        arguments = (minning.JEWEL_QUEST_CONTRACT_ADDRESS, miner_hero_ids, 1, private_key,
          w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)


      if(quest.get_min_stamina(quest_hero_ids) >= 15):
        quest_func(*arguments)

      quest_info = quest_utils.human_readable_quest(quest.get_hero_quest(quest_hero_ids[0]))

      if quest_info is None:
        logger.info(f'quest did not start. quest_type: {quest_type} sleep 20 min')
        time.sleep(60*20)
        continue

    except KeyboardInterrupt:
      break
    except:
      traceback.print_exc()
      quest_info = quest_utils.human_readable_quest(quest.get_hero_quest(quest_hero_ids[0]))
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

        tx_receipt = quest.complete_quest(quest_hero_ids[0], private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout)
        quest_result = quest.parse_complete_quest_receipt(tx_receipt)
        logger.info("Rewards: " + str(quest_result) + " sleep 3 hours.")

        # checking level up
        for i in quest_hero_ids:
          hero = heroes.get_hero(i, rpc_server)
          readable_hero = heroes.human_readable_hero(hero)
          if(readable_hero['state']['xp'] >= (readable_hero['state']['level'] + 1) * 1000):
            requests.post(settings.DISCORD_URL, { 'content': f'hero {readable_hero["id"]} has enough xp for level up' })

        time.sleep(60*60)
    except KeyboardInterrupt:
      break
    except:
      traceback.print_exc()
      time.sleep(10)
