# BTCWalletGenerator with desired patterns
# Develop By MahdiGhaemi 2023

# Imports
import os
import time
import datetime
import threading
import multiprocessing
from bitcoinlib.keys import Key, HDKey

# [config] Patterns
# [You cant use uppercase letter "O", uppercase letter "I", lowercase letter "l", and the number "0" in BTC address]
desired_patterns = ["1VioLet", "1Moon", "1MVFA", "1SoL",
                    "1Rasta", "1Zahra", "1mahdi", "1hosein",
                    "1otis", "1BLACK", "1DARK", "1Dark",
                    "1Vahid", "1Morteza", "1Reza", "1Mahdi",
                    "1rasta", "1zahra", "1python", "1btc",
                    "1BTC", "1Navid", "1ALi", "1Ghaemi", "1a"]

# [config] Search mode config
find_from_start = True
find_from_middle = False
find_from_end = False

# [config] Compare patterns insensitive
compare_case_insensitive = True

# [config] Folder/Dir for saving result
wallets_dir = "wallets"

# [config] Stop with first find
stop_with_first_find = False

# [config] Log every sec
log_time = 1

# [config] Thread counts
thread_count = multiprocessing.cpu_count() * 2

# [handle by program] Threads list
threads = list()

# [handle by program] Stop After finding a match
stop_thread = False

# [handle by program] How many try happend
try_count = 0

# Create wallets folder if not exist
if not os.path.exists(wallets_dir):
    os.makedirs(wallets_dir)


class BTCWalletGenarator(threading.Thread):
    def __init__(self,
                 desired_patterns,
                 find_from_start,
                 find_from_middle,
                 find_from_end):

        threading.Thread.__init__(self)

        self.desired_patterns = desired_patterns
        self.find_from_start = find_from_start
        self.find_from_middle = find_from_middle
        self.find_from_end = find_from_end

    def get_info(self):
        point_x, point_y = self.key.public_point()
        wallet_info = f"""
    KEY INFO
        Network                     {self.key.network.name}
        Compressed                  {self.key.compressed}

    SECRET EXPONENT
        Private Key (hex)           {self.key.private_hex}
        Private Key (long)          {self.key.secret}
        {"Private Key (wif)           %s" % self.key.wif_key() if isinstance(self.key, HDKey) else  "Private Key (wif)           %s" % self.key.wif()}

    PUBLIC KEY
        Public Key (hex)            {self.key.public_hex}
        Public Key uncompr (hex)    {self.key.public_uncompressed_hex}
        Public Key Hash160          {self.key.hash160.hex()}
        Address (b58)               {self.key.address()}

    POITS
        Point x                     {point_x}
        Point y                     {point_y}
    """
        return wallet_info

    def generate_custom_address(self):
        global try_count
        try_count += 1

        self.key = Key()
        address = self.key.address()

        for desired_pattern in self.desired_patterns:

            original_desired_pattern = desired_pattern

            if compare_case_insensitive:
                desired_pattern = desired_pattern.lower()
                address = address.lower()

            if self.find_from_start and address.startswith(desired_pattern):
                self.match_patten = original_desired_pattern
                return True

            if self.find_from_middle and desired_pattern in address:
                self.match_patten = original_desired_pattern
                return True

            if self.find_from_end and address.endswith(desired_pattern):
                self.match_patten = original_desired_pattern
                return True

        return False

    def run(self):
        global stop_thread
        while not stop_thread:

            if self.generate_custom_address():
                export_data_file_name = f"[{self.match_patten}][{time.time()}].txt"

                with open(os.path.join(wallets_dir, export_data_file_name), "w") as file:
                    file.write(self.get_info())

                print(f"Successfully found a wallet")

                if (stop_with_first_find):
                    return


if __name__ == "__main__":
    print("Starting -> program")

    # Start thereads to find
    for i in range(thread_count):
        print(f"Starting thread -> [{i}]")

        generator = BTCWalletGenarator(desired_patterns,
                                       find_from_start=find_from_start,
                                       find_from_middle=find_from_middle,
                                       find_from_end=find_from_end)

        generator.start()
        threads.append(generator)

    # Log section
    while (True):
        lives = [thread for thread in threads if thread.is_alive()]
        print(f'[{datetime.datetime.now()}] [{len(lives)}/{len(threads)}] [{try_count}] Genarating for desired patterns in BTC wallet address')

        if (len(lives) != thread_count):
            print("Ending -> program")
            stop_thread = True
            exit(0)

        time.sleep(log_time)
