# Style-Transfer-Telegram-Bot
**Style Transfer Telegram Bot based on pre-trained neural style transfer model. [ENG]**

What is Style Transfer Telegram Bot?
------------------------------------
Style Transfer Telegram Bot is my final project for the course [Deep Learning School by MIPT](https://en.dlschool.org/).

The goal was to create a telegram bot based on a NST network that can transfer the style from one image to another.

The Bot itself: `@style_transfer_simple_dimple_bot` (Telegram)

It is possible that you found the bot by tag and found it not working. The reason most likely was that I stopped supporting the bot some time after it was created.

Network
-------
I chose [pre-trained neural style transfer model from TensorFlow Hub](https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2) as the network that performs style transfer. I took a fully pre-trained model with ready-made weights and immediately made predictions based on it, without additional training for each new image. This made the response process noticeably faster, but it had a slight impact on the quality. The network has shown quite good results. In this repository all the network code is placed in a separate module called [utils.py](https://github.com/Ezjen/telegram-bot/blob/main/utils.py). All additional functions for image processing are included in the module [utils.py](https://github.com/Ezjen/telegram-bot/blob/main/utils.py).

Bot
---
I chose [aiogram](https://docs.aiogram.dev/en/latest/index.html) as the main framework for writing the bot.

You can install it by the following command:

`$ pip install -U aiogram`

The main advantage of this framework over others is asynchrony. This allows processing requests from multiple users simultaneously. 

The entire code of the bot itself is located in the module [app.py](https://github.com/Ezjen/telegram-bot/blob/main/app.py).

Setup and manual
----------------
I set up the bot via `@BotFather`, and there I got a unique token for my bot.
Thanks to BotFather's capabilities, I was able to create a more comfortable environment for working with the bot. Here's what it looks like:

/start - get basic information about the work of the bot
/cancel - delete the last loaded image
/continue - start NST model
/info - get information about owner

**.env is git-ignored, create it by yourself in a similar way to .env.example**
API_TOKEN - token from BotFather
DIR_PATH - dir project foulder 
DATA - dir with users data (content.jpg, style.jpg, result.jpg). The telegram User_id is added to the file name so that there are no conflicts with parallel requests from different users.
**Before running my code, make sure that you get your own API_TOKEN from BotFather and specify it in the file .env.**

Deploy
------


### Custom setup

All information about packages and their versions is contained in the file [requirements.txt](https://github.com/Ezjen/telegram-bot/blob/main/requirements.txt):

`$ pip3 install -r requirements.txt`

As a result, I launched the bot with the following command:

`$ python3 app.py`

Results
-------
To see the results, you can write to the bot yourself or you can view it in the [style_transfer_bot_demo](https://drive.google.com/file/d/1pGNcrFl7f_j1vuWoXpd_aANK-yyau1aE/view?usp=share_link).