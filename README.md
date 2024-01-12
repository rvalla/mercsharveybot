![logo](https://gitlab.com/rodrigovalla/mercsharveybot/-/raw/themoststable/assets/img/icon_64.png)

# MERC's Harvey Bot

This is the code for a telegram bot. The idea is to check some market data and offer some
tools to help with investment decisions.  

## online status

[**MERC's Harvey bot**](https://t.me/mercsharvey_bot) is currently on development. From time to time it will
be running in a *virtual machine* from [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/).  

## commands

Here you can see the list of available commands. Some of them allow you to pass parameters.

- **/start**: returns simply a gretting.  
- **/about**: to check information in the database.
- **/bcba**: set up a session to check stocks in Buenos Aires.  
- **/world**: set up a session to check international stocks.  
- **/setlist**: to set up a watchlist.  
- **/list**: to check the saved watchlist.  
- **/info**: to known more about the bot.  
- **/help**: returns some explanations.  
- **/language**: to set the language.  
- **/cancel**: to terminate conversation sessions.  

## running the code

Note that you will need a *config.json* file on root which includes the bot's mandatory token to run this software.
Currently *token* (provided by [@BotFather](https://t.me/BotFather), *logging* (info, debugging or persistent) and
*webhook* related data are needed:

```
{
	"bot_name": "MERC's Harvey Bot",
	"date": "2024-01-05",
	"username": "mercsharvey_bot",
	"admin_id": "A mistery",
	"link": "https://t.me/mercsharvey_bot",
	"token": "I won't tell you my token",
	"password": "Another mistery",
	"public_ip": "192.168.0.1",
	"webhook": true,
	"webhook_path": "an_url_path_for_your_webhook",
	"webhook_port": 8443,
	"logging": "info"
}

```
## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Python**](https://www.python.org/): the programming language I used.  
- [**python-telegram-bot**](https://python-telegram-bot.org/): the library I used to contact the *Telegram API*.  

Data of stock prices are retrieve from [Invertir Online](https://www.invertironline.com/). The bot waits between 1 and 5
seconds to execute each query. The idea is to get some information you need directly the go assuming you can access the
platform of your choice to get real-time information.  

Reach **MERC's Harvey bot** [here](https://t.me/mercsharvey_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
