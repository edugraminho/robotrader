import time
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *


def main():
    while True:

        connect_telegram()
        print("blas")
        time.sleep(2000)
    
main()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_messages_group(client))
# loop.close()