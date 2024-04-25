from pyhashers import hash_directory_contents

hashes = hash_directory_contents(".")
print(hashes)  