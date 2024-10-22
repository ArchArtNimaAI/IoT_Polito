# Luminet (Smart Light Controlling)
![IoT_First](https://github.com/user-attachments/assets/e09cc98d-c718-474c-89d1-3326abae060c)
## Overview
The Smart Lighting Control System is an Internet of Things(IoT) project designed to provide intelligent control and monitoring of lighting systems within a building. By automating lighting control based on various factors, such as motion detection and ambient illumination levels, the project aims to enhance energy efficiency, user comfort, and convenience.

The core component, a Controller (Arduino), orchestrates sensor data and controls the actuators responsible for the lighting. Users can interact with the system via a Telegrambot, enabling remote light control and status checks.
A JSON configuration simplifies setup, and the system allows room-level lighting control.

## Objectives
![IoT](https://github.com/user-attachments/assets/d6e838c6-1326-4a29-9ace-34644415d712)
+ Objective 1:
Implement an energy-efficient lighting control system. Promote sustainable energy use and reduce waste.
+ Objective 2:
Provide user-selectable automatic and manual lighting modes. Enable remote control and monitoring of the lighting system.
+ Objective 3:
Adjust lighting status based on ambient light conditions. Enhance user comfort and atmosphere through smart lighting. 

## Project Protocols:
+ MQTT (MessageQueuing TelemetryTransport)
+ HTTP (hypertext transfer Protocol)

## Components:
#### Sensors:
These include motion sensors (PIR) to detect movement in rooms and light sensors (LDR or ambient light sensors) to measure ambient light levels.
#### + Actuator:
These controllable light fixtures can be turned on or off based on sensor data or user commands.
#### + Controller(Arduino):
The Arduino is the system's central brain, collecting sensor data, making decisions, and controlling the actuators.
#### + Telegram Bot:
A Telegram bot allows users to interact with the system, sending commands to control the lights and receive status updates.
#### + ThingSpeak:
Customizable widgets and visualizations allow the creation of a dashboard tailored to the user's needs by adding charts, gauges, maps, and other elements to display data.

## Diagram:
![IoT_Diagram](https://github.com/user-attachments/assets/4e57e952-5bb2-4ad9-9da4-17a96109eb8a)

## TELEGRAM BOT:
I introduce a Telegram bot to control lights, update a catalog, and check sensor and light statuses. The aim is to create an interactive bot that simplifies home automation and
user monitoring tasks.  
Communication occurs through connecting the user to the IoT gateway via the HTTP paradigm. Users can easily switch ON/OFF the apartment’s light
remotely with the assistance of TelegramBot. 
![image](https://github.com/user-attachments/assets/7da180ab-e560-4d81-b059-53553ed4bb11)

### USER INTERFACE (Telegram Bot):
#### + Bot Functionalities:
Starting the bot is crucial, and we achieve this using the start() method, initiating a message loop. Users can interact with the bot using commands like /start and receive a keyboard menu for various actions.
#### + Updating the Catalog:
The catalog is the central data structure managed by our bot. Different sections allow users to add or remove sensor and actuator details, enhancing home automation customization.
#### + Querying Data:
Our bot offers features to control lights, check light status, and monitor sensor data. It communicates with external services via HTTP requests to fetch real-time status information. The bot's capabilities extend to multiple rooms, providing flexibility for users to manage various spaces.
#### + Data Structure:
The catalog.json file holds the catalog's data structure. Each key-value pair within the catalog serves a specific purpose, defining the properties of sensors, actuators, and their configurations. Understanding this structure is key to effectively managing
home automation.
![Telegram](https://github.com/user-attachments/assets/6d8dae76-3513-4e7f-985f-a90cc3f59ed0)

### USER INTERFACE (Dashboard):
ThingSpeak is an open-source IoT platform that allows you to collect, store, and analyze data from IoT devices. It offers some key features:
#### + Visualization: 
You can create customizable dashboards and visualizations to monitor and analyze the data from your IoT devices.
#### + Alerts and Notifications: 
ThingSpeak supports triggers and alerts, enabling you to set up notifications based on certain conditions or thresholds in your data.
#### + Integration:
It integrates with other IoT platforms and services, making it versatile for various IoT applications.
![image](https://github.com/user-attachments/assets/e7cb4bb0-b7c3-4987-9db7-f4add94d759e) ![image](https://github.com/user-attachments/assets/c452da4e-0058-4761-b7e9-04b4496ca9be)
![image](https://github.com/user-attachments/assets/4e4c5b95-483c-458e-b64d-7776d310980a)
