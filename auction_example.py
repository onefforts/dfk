import logging
import sys
import settings
import auctions.sale.sale_auctions as sales
import auctions.rent.rent_auctions as rental
from web3 import Web3


if __name__ == "__main__":
    log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'

    logger = logging.getLogger("DFK-auctions")
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

    rpc_server = 'https://api.harmony.one'
    logger.info("Using RPC server " + rpc_server)

    graphql = 'http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv6'

    private_key = settings.PRIVATE_KEY  # set private key
    gas_price_gwei = 31
    tx_timeout = 60
    w3 = Web3(Web3.HTTPProvider(rpc_server))
    account_address = w3.eth.account.privateKeyToAccount(private_key).address

    sell_price = 70

    #sales.create_auction(102244, sales.ether2wei(sell_price), sales.ether2wei(sell_price), 60, "0x0000000000000000000000000000000000000000", private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout, rpc_server, logger)
    sales.cancel_auction(102244, private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, tx_timeout, rpc_server, logger)

#    auctions = sales.get_open_auctions(graphql, 0, 10)
#    logger.info("Sale auctions:")
#    for auction in auctions:
#        logger.info(str(auction))
#
#    # sales.bid_hero(hero_id, ether2wei(100), prv_key, nonce, gas_price_gwei, 30, rpc_server, logger)
#
#    logger.info("\n")
#    logger.info("Rental auctions:")
#    auctions = rental.get_open_auctions(graphql, 0, 10)
#    for auction in auctions:
#        logger.info(str(auction))
