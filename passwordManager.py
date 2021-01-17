import hashlib
import secrets
import csv

CSV_FILE = "passwords.csv"
MASTER_HASH_FILE = "master.txt"

def masterHashComapare(password):
    master = open(MASTER_HASH_FILE)
    hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    if (hash == master.read()):
        return True
    else:
        return False

def createMasterHashFile(password):
    with open(CSV_FILE, mode='w') as password_file:
        password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
        password_writer.writerow(["site", "username", "salt", "hash"])
    master = open(MASTER_HASH_FILE, 'w')
    hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    master.write(hash)

def hashPassword(password):
    salt = secrets.token_hex(64)
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    return salt,hash

def writeCsv(site, username, salt, hash):
    try:
        readCsv("site")
    except FileNotFoundError:
        with open(CSV_FILE, mode='a') as password_file:
            password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
            password_writer.writerow(["site", "username", "salt", "hash"])
    with open(CSV_FILE, mode='a') as password_file:
            password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
            password_writer.writerow([site, username, salt, hash])

def readCsv(site):
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        line_count = 0
        for row in password_reader:
            if(line_count != 0):
                if (row[0] == site):
                    return row
            line_count += 1

def deleteCsv(site):
    changes = list()
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        for row in password_reader:
            if (row[0] != site):
                changes.append(row)

    with open(CSV_FILE, mode="w") as password_file:
        password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
        password_writer.writerows(changes)
            
def listSites():
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        sites = list()
        line_count = 0
        for row in password_reader:
            if (line_count != 0):
                sites.append(row[0])
            line_count += 1
    return sites

def menu():
    print("BENN'S PASSWORD MANAGER")
    print("-----------------------")
    print("1. Create password")
    print("2. Retrive password")
    print("3. Delete password")
    print("4. List Sites")
    print("5. Quit")
    print("-----------------------\n")

    userInput = int(input("Enter option: "))
    return userInput

passwordAttempts = 0
while(True):
    try:
        password = input("Enter master password: ")
        if(not masterHashComapare(password)):
            if (passwordAttempts > 1):
                print("\n**TOO MANY WRONG ATTEMPTS**\n")
                raise SystemExit(0)
            else:
                print("\n**WRONG PASSWORD**\n")
                passwordAttempts += 1
                continue
        else:
            print("\nPASSWORD CORRECT\n")
            break
    except FileNotFoundError:
        print("\nMaster password file doesn't exist. Creating master file. Initializing Database.\n")
        createMasterHashFile(password)
        break

while(True):
    choice = menu()
    if (choice < 1 or choice > 5):
        print("\n**INVALID OPTION**\n")
        continue

    if (choice == 1):
        site = input("Enter site name: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        try:
            if (readCsv(site) != None):
                print("\n**SITE ALREADY EXISTS**\n")
                continue
        except FileNotFoundError:
            pass
        username = input("Enter username for %s: " % site)
        password = input("Enter simple password to be hashed: ")
        hashTuple = hashPassword(password)
        writeCsv(site, username, hashTuple[0], hashTuple[1])
        print("\nPASSWORD HASHED AND SAVED SUCCESSFULLY\n")

    if (choice == 2):
        site  = input("Enter site to retrive: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        try:
            if (readCsv(site) == None):
                print("\n**NO SITE FOUND**\n")
                continue
            else:
                csvRow = readCsv(site)
                print("\n")
                print("SITE: %s" % csvRow[0])
                print("USERNAME: %s" % csvRow[1])
                print("PASSWORD: %s" % csvRow[3])
                print("\n")
        except FileNotFoundError:
            print("\n**PASSWORD FILE DOES NOT EXIST, CREATE PASSWORD**\n")
            continue
    if (choice == 3):
        site = input("Enter site to delete: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        if (readCsv(site) == None):
            print("\n**NO SITE FOUND**\n")
            continue
        else:
            deleteCsv(site)
            print("\nSITE DELETED SUCCESSFULLY\n")
    
    if (choice == 4):
        if (listSites()):
            counter = 1
            print("\n")
            for site in listSites():
                print("%i: %s" % (counter,site))
                counter += 1
            print("\n")
        else:
            print("\nNO SITES IN FILE\n")
        

    if (choice == 5):
        print("\nGOODBYE! :)\n")
        break
