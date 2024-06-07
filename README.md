# Password Manager With Fingerprint Auth
Secured through the master password!
**Device Used: **

Macbook (MacOS) 
## How to Run: 
### Dependencies: 
```pip3 install the dependencies```

### Fingerprint Reader:
Ensure that your device has a fingerprint reader

### Run the command 
```python3 main.py```


# About the Project 

## **Biometric Authentication **
If you click “Use Password…” it will initiate a trap interrupt to close the application, enforcing fingerprint authentication (biometrics) as the only way to pass through this phase. 
It will only let you authenticate if you have the right fingerprint. 

## **Sign Up **
If it's your first time using this app, it will prompt you to sign up to create your master password. The master password will be encrypted with the bcrypt algorithm with a work factor of 15, stored in the json file, /passwords/master_password.json. 

You will have to insert your password twice to ensure they match, as this is unable to be changed. 

The password should also be very strong as if someone knows the master password, they will be able to decrypt your other passwords. 

Because it is encrypted, it can only be brute-forced to get in, and the work factor of 15 helps prevent this. 

## **Login**
With more than 5 unsuccessful login attempts, it kicks you out of the session and closes the window. This helps prevent brute force attacks as you would have to re-authenticate with an authorized fingerprint. 

## **Home Page**

This is the homepage of the application once the user is successfully authenticated. It displays all of the passwords, with useful features such as:

1. Generating Password
2. Adding New Password
3. Copying Password (to clipboard) 
4. Updating Password
5. Deleting Password 

The regular passwords are encrypted/ hashed with a key that is generated using the master password. The key and master password will be stored in the heap, and will only persist for the duration of the application when it is opened. The passwords are also salted to mitigate hash table attacks by forcing attackers to re-compute them using the salts for each password.

In the code, password.py: 


```
   def derive_key(self, master_password, salt):
       salt = base64.urlsafe_b64decode(salt)
       kdf = PBKDF2HMAC(
           algorithm=hashes.SHA256(),
           length=32,
           salt=salt,
           iterations=100000,
           backend=default_backend()
       )
       key = kdf.derive(master_password.encode())
       return base64.urlsafe_b64encode(key)
```


This creates a symmetric/ secret key that is generated using the master password. Therefore, without knowing the master password, it will not be able to decrypt the other regular passwords. 

## **Generate Password**

Generates a random password with numbers 0-9, and letters “A-Z” both capitalized and lowercase, and symbols ['@', '#', '$', '%', '&', '_']. The generated password will be in the heap until the password generator is closed. 

A random password generator is very useful because people are horrible at creating passwords, so having a random password generator is a great addition and feature to the password manager. 
