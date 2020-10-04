The program is a simple password manager that stores and retrieves passwords for a bunch of websites. It stores them with a master password. Also, it uses hashing with a 'SALt' (a key) and the website name to avoid brute force attack.
In this code, the user has to give website url as an argument. The code then asks for a master password. If the master password is correct, the code checks if website is already on the DB. If not, if creates a new record. Otherwise, it displays the respective password on DB.



To run the program, one must have python3 installed in their system. 
Also, they need bcrypt. You can run the following command in the command line rompt if it is not already on the system.
'pip install bcrypt'
Next type the command to run the python program. 
'python3 pwMan.py <website url>'
In my case the program was saved in the C folder. Make sure you have the path right before you execute the code.

