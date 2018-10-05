# Surakshit
This project was created for SNU HackData 2.0 2018. The motive behind the project was to create a decentralized emergency services 
providing system which could connect the needy directly to the nearest authority concerned with a particular type of emergencies, viz.,
fire, police or ambulance. 

This project was realized using the [Telegram bot API for Python](https://github.com/python-telegram-bot/python-telegram-bot).

## How to Use
#### Authority Side - Suraksha bot
First, the authority has to register themselves using the **Suraksha** bot, once they are registered, they'll start receiving the request from the nearest user.
#### User Side - Surakshit bot
The user can send all the necessary details about the emergency from the **Surakshit** bot to the nearest authority. 

We used **Firebase** to store registrations from the Suraksha bot and **Haversine Formula** for calculating the nearest distance.
