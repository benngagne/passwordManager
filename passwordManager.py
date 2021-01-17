import hashlib
import secrets
import csv

CSV_FILE = "passwords.csv"

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
            

def menu():
    print("BENN'S PASSWORD MANAGER")
    print("-----------------------")
    print("1. Create password")
    print("2. Retrive password")
    print("3. Delete password")
    print("4. Quit")
    print("-----------------------\n")

    userInput = int(input("Enter option: "))
    return userInput
 

while(True):
    choice = menu()   
    if (choice < 1 or choice > 4):
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
        print("\nGOODBYE! :)\n")
        break
