![logo](https://gitlab.com/azarte/azarte.gitlab.io/-/raw/master/public/assets/img/logo_64.png)

# MERC's Harvey Bot: changelog

## 2024-03-07: v0.5 beta

Now the language preference is saved at *context.chat_data*. The *watchlist* implementation
was completely redesign. Now is possible to set several watchlists. Related commands were
updated:
- **watchlists**: the command to check user's watchlists (it was **list** before).
- **setwatchlist**: the commnand to set a new watchlist (it was **setlist** before).
- **erasewatchlist**: the command to erase a watchlist.

## 2024-01-31: v0.3.1 beta

New *random selection messages* to make **/setlist** more funny. Updated database.  

## 2024-01-16: v0.3 beta

The **bot** has a new **/dolar** command. New symbols were added to the database.  

## 2024-01-12: v0.2 beta

The **bot** is running now. There are several improvements for this *beta* state.
The users can set up a watchlist now (there is a new **Users()** class related to that).
I added some animated emojis to get more beautiful messages.

New commands:

- **setlist**: to set up a watchlist.
- **list**: to check your watchlist.
- **info**: to print extra information about the bot.

## 2024-01-05: v0.1 alpha

First steps setting the bot. The **bot** is in
*bot.py* file but use a set of classes.  

The **bot** initial commands are:

- **/start**: returns simply a gretting.  
- **/about**: to check information in the database.
- **/bcba**: set up a session to check stocks in Buenos Aires.  
- **/world**: set up a session to check international stocks.  
- **/help**: returns some explanations.  
- **/language**: to set the language.  
- **/cancel**: to terminate conversation sessions.    

Reach **MERC's Harvey bot** [here](https://t.me/mercsharvey_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
