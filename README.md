![logo](https://gitlab.com/azarte/azarte.gitlab.io/-/raw/master/public/assets/img/logo_64.png)

# MERC's Harvey Bot

This is the code for a telegram bot. The idea is to check some market data and offer some
tools to help with investment decisions.  

## online status

[**MERC's Harvey bot**](https://t.me/mercsharvey_bot) is currently on development. From time to time it will
be running in a *virtual machine* from [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/).  

## commands

Here you can see the list of available commands. Some of them allow you to pass parameters.

- **/start**: returns simply a greeting.  
- **/color**: starts the visual alternatives.
- **/text**: starts the textual alternatives.  
- **/noise**: starts the auditive alternatives.  
- **/interaction**: the bot creates from something you send.
- **/genuary**: the command to enter the artificially generated month of time where we build code that makes beautiful things.  
- **/number f**: returns a random number rolling a dice with *f* faces.  
- **/sequence f n**: returns a random sequence of *n* numbers rolling a dice with *f* faces.  
- **/choice a b c**: returns a random word from your message.
- **/qatar teama teamb**: the bot propose a result for a football match.  
- **/language**: to set the bot language, Spanish (default) or English.
- **/help**: returns a link to bring you here.  

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

Proprietary software has helped here too. I must especially mention [DeepL translator](https://www.deepl.com/translator).
Even though I know English, it has helped me a lot to translate the content of **azarte_bot**.  

Data of stock prices are retrieve from [Invertir Online](https://www.invertironline.com/). The bot waits between 1 and 5
seconds to execute each query. The idea is to get some information you need directly the go assuming you can access the
platform of your choice to get real-time information.  

Reach **MERC's Harvey bot** [here](https://t.me/mercsharvey_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
