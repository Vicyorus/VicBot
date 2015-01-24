VicBot
======

A chat bot/logger for Wikia Chats built on Python 2.7

This project is heavily influenced by [chatbot-rb](https://github.com/sactage/chatbot-rb) from [sactage](https://github.com/sactage) and uses a modified version of [hairr](https://github.com/hairr)'s [chatbot](https://github.com/hairr/chatbot) module as the client.

Installation
-------------

* Install Python 2.7.
* Install the requests module (`[sudo] pip install requests`).
* Create a `config.json` file (use `config.sample.json` as a reference).
* Run vicbot.py (`[python] vicbot.py`).

Commands
---------

|Command | Function
|------|----------
| `!hon` | Turns the `!hello` command on.
| `!hoff` | Turns the `!hello` command off.
| `!yton` | Turns YouTube video information on.
| `!ytoff` | Turns YouTube video information off.
| `!lon` | Turns logging on.
| `!loff` | Turns logging off. Updates logs before shutting off.
| `!seenon` | Turns the `!seen` command on.
| `!seenoff` | Turns the `!seen` command off.
| `!twon` | Turns Twitter tweet information on.
| `!twoff` | Turns Twitter tweet information off.
| `!tellon` | Turns the `!tell` command on.
| `!telloff` | Turns the `!tell` command off.
| `!hello [message]` | Says "Hello". If followed by `message`, will say "Hello, `message`".
| `!bye` | Says "Goodbye!".
| `!quit` | Makes the bot exit the chat.
| `!updated` | Gives information about how long ago were the logs updated and how many lines are in disk.
| `!logs` | Links the logs page.
| `!dumpbuffer` | Clears the logfile.
| `!seen user` | Gives the last time the bot "saw" the `user`.
| `!kick user` | Kicks `user` from chat.
| `!updatelogs` | Updates the logs.
| `!gauss x, y, z` | Gives the sum of all the numbers from `x` to `y` with a common difference of `z`. 
| `!ignore user` | Makes the bot ignore any commands used by `user`.
| `!unignore user` | Makes the bot accept any command used by `user`.
| `!tell user message` | Sends a `message` to `user` the next time the bot sees them.
