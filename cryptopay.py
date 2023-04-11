from aiocryptopay import AioCryptoPay, Networks
load_dotenv()
crypto = AioCryptoPay(token=os.getenv("CRYPTOPAY_KEY"), network=Networks.MAIN_NET)
