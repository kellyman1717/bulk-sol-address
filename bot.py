import time
import sys
import os
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum
from solana.keypair import Keypair
import base58

def animate_creating(duration):
    end_time = time.time() + duration
    spinner = ['|', '/', '-', '\\']
    i = 0
    while time.time() < end_time:
        sys.stdout.write('\rMembuat address... ' + spinner[i % 4])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 30 + '\r')

def generate_solana_address():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    solana_seed = seed[:32]
    kp = Keypair.from_seed(solana_seed)
    address = str(kp.public_key)
    private_key = base58.b58encode(kp.secret_key).decode()
    seed_phrase = mnemonic
    return address, private_key, seed_phrase

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("    ╔═══════════════════════════════════════════════╗")
        print("    ║                                               ║")
        print("    ║        AUTO GENERATE BULK SOLANA ADDRESS      ║")
        print("    ║                                               ║")
        print("    ╚═══════════════════════════════════════════════╝")
        print()
        print("1.Buat Random Bulk Solana Address")
        print("2.Tampilkan Address Solana yang Sudah Dibuat")
        print("0.Keluar")
        choice = input("\nPilih menu: ")

        if choice == '1':
            try:
                jumlah = int(input("\nMasukkan jumlah address yang ingin dibuat: "))
                animate_creating(2)
                
                # Get the last number from existing file
                start_number = 1
                if os.path.exists('address_sol.txt'):
                    with open('address_sol.txt', 'r') as f:
                        content = f.read()
                        existing_numbers = [int(x.split('.')[0]) for x in content.split('No.')[1:]]
                        if existing_numbers:
                            start_number = max(existing_numbers) + 1
                
                with open('address_sol.txt', 'a') as f:
                    for i in range(jumlah):
                        address, private_key, seed_phrase = generate_solana_address()
                        f.write(f"No.{start_number + i}\n")
                        f.write(f"Address: {address}\n")
                        f.write(f"Private Key: {private_key}\n")
                        f.write(f"Seed Phrase: {seed_phrase}\n")
                        f.write("-" * 50 + "\n\n")
                print(f"\n{jumlah} Address telah dibuat dan disimpan di address_sol.txt")
            except ValueError:
                print("Masukkan angka yang valid!")
            input("\nTekan Enter untuk kembali ke menu utama...")
        elif choice == '2':
            try:
                with open('address_sol.txt', 'r') as f:
                    content = f.read().strip()
                    if not content:
                        print("\nKamu belum membuat address sebelumnya")
                    else:
                        print("\nMenampilkan address dari file address_sol.txt:\n")
                        print(content)
            except FileNotFoundError:
                print("\nKamu belum membuat address sebelumnya")
            input("\nTekan Enter untuk kembali ke menu utama...")
        elif choice == '0':
            print("\nExiting....", end='', flush=True)
            time.sleep(1.2)
            print("\n")
            break
        else:
            print("\nPilihan tidak valid")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()