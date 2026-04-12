from algosdk import account, mnemonic

private_key, address = account.generate_account()

print("PUBLIC ADDRESS:")
print(address)

print("\nMNEMONIC (SAVE THIS SECURELY):")
print(mnemonic.from_private_key(private_key))

