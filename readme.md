# **1. COMPILATION**
``pyinstaller --onefile 
--add-data "config.py;." 
--add-data "helpers;helpers" 
--add-data "controllers;controllers" 
--hidden-import=paramiko 
--hidden-import=pyTelegramBotAPI 
--hidden-import=telebot 
main.py``

# **2. USAGE**
``cd dist`` </br>
``./main --username USERNAME --password PASSWORD --server_ip SERVER_IP --token BOT_TOKEN --secret_phrase SECRET_PHRASE --user_id USER_ID``

# **3. BOT INSTRUCTION**
Send phrase to bot and bot will send you information about your server. </br>