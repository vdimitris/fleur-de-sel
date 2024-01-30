# Fleur de sel ...for hashing salted passwords
This is the experimental code and some results of my recently (Jan. 2024) started research on creating a better salt in order to make hashed salted passwords more resistant to brute force attacks using dictionaries and rainbow tables.

The 'scenario.py' script runs a scenario and saves the results that can be viewed later using the 'view-results.py' script. Results data sets have 3 columns:

- the first column is just an id for the row (it is the round number)
- on the second column you can find the values of the authentication system time
- on the third column you can find the values of the time an attacker needed to succeed

todo: write more info about the Fleur de sel (Fds) concept 