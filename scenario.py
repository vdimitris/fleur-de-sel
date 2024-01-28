import itertools
import random
import string
import hashlib
import time
from matplotlib import pyplot
import numpy

# create random wordlist with words (number of words) and length (length of each word)
# it is used by the attacker

def create_wordlist(words, length):
    
    wordlist = open("wordlist.txt", "w")
    characters = string.ascii_letters + string.digits + string.punctuation
    counter = set()

    for i in range(0, words):

        random_string = ''.join(random.choice(characters) for i in range(length))
        wordlist.write(random_string + "\n")
        counter.add(random_string)

    wordlist.close()

    print("wordlist created with", len(counter), "unique words")

# choose random word from wordlist to use as password for user
# the user selected a common password so the brute force attacker will succeed 

def choose_random_password():

    wordlist = open('wordlist.txt', 'r')
    passwords = wordlist.readlines()
    password = random.choice(passwords).strip("\n")
    print("Selected password for test account:", password)

    return password

# create salts for the user account

def create_salts(number, length):

    salts = []
    characters = string.ascii_letters + string.digits

    for i in range(0, number):

        random_string = ''.join(random.choice(characters) for i in range(length))
        salts.append(random_string)
    
    print("Salts:", salts)

    return salts

# choose random salt from salts and hash the password
# salts_combo : number of salts to use from the salts pool

def choose_random_salt(salts, salts_combo):

    if salts_combo == 1:

        selected_random_salt = random.choice(salts)
        print("Selected salt:", selected_random_salt)

    else:

        salt_combinations = list(itertools.combinations(salts, salts_combo))
    
        selected_random_salt = random.choice(salt_combinations)
        print("Selected salt:", selected_random_salt)
    
    return selected_random_salt

# hash the password with selected salt

def password_hash(password, selected_random_salt, salts_combo):

    password_salt = password

    if salts_combo == 1:

        password_salt = password_salt + selected_random_salt

    else:

        for salt in selected_random_salt:

            password_salt = password_salt + salt

    print("Password+Salt:", password_salt)
    password_hash = hashlib.sha256(password_salt.encode('UTF-8'))
    password_hash_hex = password_hash.hexdigest()
    print("SHA-256 output:", password_hash_hex)

    return password_hash_hex

# brute force attempt by the system (password provided by user)

def brute_force_system(password, salts, salts_combo, password_hash_hex):

    print("*** user ***")

    user_password = password    # user provided the correct password

    if salts_combo == 1:

        for salt in salts:

            try_password_salt = user_password + salt
            try_password_hash = hashlib.sha256(try_password_salt.encode('UTF-8'))
            try_password_hash_hex = try_password_hash.hexdigest()
            
            if try_password_hash_hex == password_hash_hex:

                print("Login ok, using salt:", salt)
                break
    else:

        salt_combinations = list(itertools.combinations(salts, salts_combo))

        for salt in salt_combinations:

            multi_salt = ""

            for salt_part in salt:
                
                multi_salt = multi_salt + salt_part

            try_password_salt = password + multi_salt

            try_password_hash = hashlib.sha256(try_password_salt.encode('UTF-8'))
            try_password_hash_hex = try_password_hash.hexdigest()
        
            if try_password_hash_hex == password_hash_hex:

                print("Login ok, using salt:", salt)
                break        
    

# brute force attack by the attacker (password guessing with wordlist)
# knowing salts and hashed salted password

def brute_force_attacker(salts, salts_combo, password_hash_hex):

    print("*** attacker ***")

    wordlist = open('wordlist.txt', 'r')
    passwords = wordlist.readlines()

    password_found = False

    if salts_combo == 1:    # the easy way

        for salt in salts:

            if password_found: break

            for password in passwords:

                try_password_salt = password.strip("\n") + salt
                try_password_hash = hashlib.sha256(try_password_salt.encode('UTF-8'))
                try_password_hash_hex = try_password_hash.hexdigest()
                
                if try_password_hash_hex == password_hash_hex:

                    print("found the password:", password.strip("\n"))
                    print("using salt:", salt)
                    password_found = True
                    break

    else:   # the Fleur Del Sel way

        salt_combinations = list(itertools.combinations(salts, salts_combo))

        for salt in salt_combinations:

            if password_found: break

            multi_salt = ""

            for salt_part in salt:
                
                multi_salt = multi_salt + salt_part         
                
            for password in passwords:

                try_password_salt = password.strip("\n") + multi_salt
                try_password_hash = hashlib.sha256(try_password_salt.encode('UTF-8'))
                try_password_hash_hex = try_password_hash.hexdigest()
                
                if try_password_hash_hex == password_hash_hex:

                    print("found the password:", password.strip("\n"))
                    print("using salt:", salt)
                    password_found = True
                    break

    wordlist.close()

# run a scenario

def scenario(scenario_details):

    salts_number = scenario_details[0]      # pool of salts
    salts_length = scenario_details[1]
    salts_combo = scenario_details[2]       # how many salts to use from the pool

    password = choose_random_password() # from existing words in wordlist

    salts = create_salts(salts_number, salts_length)

    selected_random_salt = choose_random_salt(salts, salts_combo)

    password_hash_hex = password_hash(password, selected_random_salt, salts_combo)

    start_time = time.time() 
    result_system = brute_force_system(password, salts, salts_combo, password_hash_hex)
    system_time = time.time() - start_time
    print("verified in %s seconds" % system_time)

    start_time = time.time() 
    brute_force_attacker(salts, salts_combo, password_hash_hex)
    attacker_time = time.time() - start_time
    print("password attack for %s seconds" % attacker_time)

    return [system_time, attacker_time]

# start main logic

# #############################################################
# various scenarios details
# format for scenario details...
# scenario_details = [salts_number, salts_length, salts_combo]
# #############################################################

# scenario_details = [1, 7, 1]      # scenario 1: 1 possible salt of 7 chars, using 1 salt

# scenario_details = [5, 7, 1]      # scenario 2: 5 possible salts of 7 chars, using 1 salt

scenario_details = [15, 7, 1]     # scenario 3: 15 possible salts of 7 chars, using 1 salt

# scenario_details = [50, 7, 1]     # scenario 4: 50 possible salts of 7 chars, using 1 salt

# scenario_details = [15, 7, 2]     # scenario 5: 15 possible salts of 7 chars, using compbination of 2 salts

# init wordlist

wordlist_size = 1000000
words_length = 15

create_wordlist(wordlist_size, words_length)

# repeat scenario

rounds = 100    # how many rounds to repeat the scenario

results = []    # execution times for (system, attacker)

for i in range(1,rounds + 1):

    print("########### round", i, "#############")
    times = scenario(scenario_details)
    times[:0] = [i]     # add an id column
    results.append(times)

# print(results)

numpy.set_printoptions(suppress=True)

plot_results = numpy.array([numpy.array(i) for i in results])

print(plot_results)

means = numpy.mean(plot_results, axis = 0)

print("system time mean:", f'{means[1]:.7f}')
print("attacker time mean:", f'{means[2]:.7f}')

export_filename = "results/scenario_" + str(wordlist_size) + "_" +\
                                        str(words_length) + "_" +\
                                        str(scenario_details[0]) + "_" +\
                                        str(scenario_details[1]) + "_" +\
                                        str(scenario_details[2]) + "-" +\
                                        "rounds-" + str(rounds) + ".txt"

numpy.savetxt(export_filename, plot_results)

# results to plot

pyplot.plot(plot_results[:,0], plot_results[:,1], marker = "o", color = "blue", label = "system")
pyplot.plot(plot_results[:,0], plot_results[:,2], marker = "o", color = "red", label = "attacker")   
pyplot.xlabel("# try")
pyplot.ylabel("duration (sec)")
pyplot.legend()
pyplot.show()
