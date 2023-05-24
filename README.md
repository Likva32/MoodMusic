#  MoodMusic - Bagrut final project

## how to setup

### setting up sending code by mail
### First step - creating code
![image](https://github.com/Likva32/MoodMusic/assets/114340841/7484bd50-99d5-497f-90b9-453b5f215e46)
![image](https://github.com/Likva32/MoodMusic/assets/114340841/f31d2a91-81c6-47dc-9758-160e864e96e0)


### turn on 2fa
![image](https://github.com/Likva32/MoodMusic/assets/114340841/a3c99450-5b88-4d12-9770-12d3e5bc2fbc)

#### after this enter this address:  myaccount.google.com/u/3/apppasswords

#### After typing the password, you need to create an "app", after creating an app (in select device choose other) you will receive a code that you will need (this code is a password that will allow you to enter the user without 2fa)

![image](https://github.com/Likva32/MoodMusic/assets/114340841/f8784c78-e91d-4782-86ce-7a12863ea475)
![image](https://github.com/Likva32/MoodMusic/assets/114340841/12cc834e-b01e-43cf-87a8-2075d1d4b239)




### second step - Python code 
#### (UUID for a unique ID which is the code for password recovery (you don't need it for sending the email))
![image](https://github.com/Likva32/MoodMusic/assets/114340841/eba17191-0f49-4cb3-bffa-de476839eaae)

#### In email_password, put the code we received on Google "App"
![image](https://github.com/Likva32/MoodMusic/assets/114340841/4bc43a9b-4f52-4775-8824-1deac3a045f0)

#### Subject - string (the subject of the letter (title)) 
#### Body - string (content of the letter)
![image](https://github.com/Likva32/MoodMusic/assets/114340841/1e2b3dc8-b7e4-49b7-899a-1f541351eedc)


#### (sll is a protocol for secure communication between a browser and a website. It allows you to transfer data in an encrypted form)
![image](https://github.com/Likva32/MoodMusic/assets/114340841/9b7518b5-1744-4228-a6e8-e0c5fd8807d9)


#### The actual sending of the email
![image](https://github.com/Likva32/MoodMusic/assets/114340841/7804542d-40d0-4139-bd38-975a860ec02f)




## Set Spotify authentication app



## how to run 
### Server
#### in cmd : ...code\server> python Server.py local\IP Port
![image](https://github.com/Likva32/MoodMusic/assets/114340841/307d88e1-eea9-4567-9527-c8d960b4409f)

### Client
#### in cmd : ...code\client> python Login.py local\IP Port
![image](https://github.com/Likva32/MoodMusic/assets/114340841/6b6cf79a-7d70-4558-a788-cc401a6c6ed7)

