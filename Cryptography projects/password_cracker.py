import hashlib

# Define the read_and_add_to_arr function
def read_and_add_to_arr(file_name, arr):
    with open(file_name, "rb") as f:
        line = f.readline().strip()
        while line:
            arr.append(line)
            line = f.readline().strip()

def crack_sha1_hash(hash, use_salts=False):
    password_arr = []
    read_and_add_to_arr("top-10000-passwords.txt", password_arr)

    if use_salts:
        top_salt_passwords = {}
        top_salts = []
        read_and_add_to_arr("known-salts.txt", top_salts)
        for bsalt in top_salts:
            for bpassword in password_arr:
                prepended = hashlib.sha1(bsalt + bpassword).hexdigest()
                appended = hashlib.sha1(bpassword + bsalt).hexdigest()
                top_salt_passwords[prepended] = bpassword.decode("utf-8")
                top_salt_passwords[appended] = bpassword.decode("utf-8")
        if hash in top_salt_passwords:
            return top_salt_passwords[hash]

    passwords_dict = {}
    for p in password_arr:
        hash_line = hashlib.sha1(p).hexdigest()
        passwords_dict[hash_line] = p.decode("utf-8")

    if hash in passwords_dict:
        return passwords_dict[hash]

    return "PASSWORD NOT IN DATABASE"


# Test the function
hashed_password = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"  # Example SHA-1 hashed password
print(crack_sha1_hash(hashed_password))  # Output the cracked password
