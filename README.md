# ChatGPT, DALL·E, Stable Diffusion Telegram bot

## Table of Contents

+ [About](#about)
+ [Start](#start)
+ [ChatGPT](#chatgpt)
+ [DALL·E](#dalle)
+ [Stable Diffusion](#stablediffusion)
+ [Account and buy](#accountbuy)
+ [API tokens](#apitokens)
+ [Database](#database)
+ [How to deploy](#howtodeploy)
+ [License](#license)

## About <a name = "about"></a>

Nowadays neural networks are able to conduct a dialogue, quickly search for the information we need, answer questions and draw pictures from words. This is a Telegram bot written in Python that allows you to chat with ChatGPT and generate images using DALL·E and Stable Diffusion, payments are implemented using Crypto Bot. I think it is very comfortable to unite these neural networks in one Telegram bot.

## Start <a name = "start"></a>
When the user enters the start command, the bot sends him a welcome message stating that the user has free 3000 ChatGPT tokens, 3 DALL·E image generations and 3 Stable Diffusion image generations and displays 4 buttons: "💭Chatting — ChatGPT-4o", "🌄Image generation — DALL·E 3", "🌅Image generation — Stable Diffusion 3" and "👤My account | 💰Buy". If the user is already registered, the bot only displays buttons.

![Видео без названия — сделано в Clipchamp (5)](https://github.com/user-attachments/assets/7797790f-81de-44be-aa6b-08b2401c85c2)

## ChatGPT <a name = "chatgpt"></a>
If the user wants to chat with ChatGPT, he presses the "💭Chatting — ChatGPT" button and chats.

This bot saves the context of the dialogue!

![Видео без названия — сделано в Clipchamp](https://github.com/user-attachments/assets/aa116f40-60ec-40dd-a137-94767b895666)

In [openaitools.py](https://github.com/vladislav-bordiug/ChatGPT_DALL_E_StableDiffusion_Telegram_Bot/blob/main/openaitools.py) in the OpenAiTools class there are three parameters in the get_chatgpt function:

```model``` - The model which is used for generation.

```max_tokens``` - The maximum number of tokens that can be generated in the chat completion.

```temperature``` - What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

## DALL·E <a name = "dalle"></a>
If the user wants to generate image with DALL·E, he presses the "🌄Image generation — DALL·E" button and generates.

![Видео без названия — сделано в Clipchamp (1)](https://github.com/user-attachments/assets/52e18bf1-ded4-406e-94f4-8fa5d5de6ffe)

Generated image:

![image](https://github.com/user-attachments/assets/5fe18110-5fb3-4a73-b66c-0a34b3a1f8fc)

In [openaitools.py](https://github.com/vladislav-bordiug/ChatGPT_DALL_E_StableDiffusion_Telegram_Bot/blob/main/openaitools.py) in the OpenAiTools class there are three parameters in the get_dalle function:

```model``` - The model which is used for generation.

```n``` - The number of images to generate. Must be between 1 and 10.

```size``` - The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.

## Stable Diffusion <a name = "stablediffusion"></a>
If the user wants to generate image with Stable Diffusion, he presses the "🌅Image generation — Stable Diffusion" button and generates.

![Видео без названия — сделано в Clipchamp (2)](https://github.com/user-attachments/assets/216214b7-7c0e-4baf-b399-fa6081e86142)

Generated image:

![image](https://github.com/user-attachments/assets/965fe6d3-ef9d-48e6-a096-209ec470694d)

In [stablediffusion.py](https://github.com/vladislav-bordiug/ChatGPT_DALL_E_StableDiffusion_Telegram_Bot/blob/main/stablediffusion.py) there is one parameter:

```model``` - The model to use for generation: sd3-medium requires 3.5 credits per generation, sd3-large requires 6.5 credits per generation, sd3-large-turbo requires 4 credits per generation.

## Account and buy <a name = "accountbuy"></a>
If the user wants to see account information or buy tokens and generations, he presses the "👤My account | 💰Buy" button. After pressing the button, the bot displays information about the rest of the user's ChatGPT tokens, DALL·E image generations and Stable Diffusion image generations. If the user wants to buy tokens and generations, he presses the "💰Buy tokens and generations" button, selects the product and currency. After that, the user needs to press the "💰Buy" button and pay in Crypto Bot if he wants to pay. If the user has paid, he should press "☑️Check" button and tokens or image generations will be added to his account. If the user hasn't paid, the bot will display the message "⌚️We have not received payment yet".

Payments are processed via webhooks.

![Видео без названия — сделано в Clipchamp (4)](https://github.com/user-attachments/assets/24980ebf-cde4-4603-9d47-6a57f43e189a)

## API tokens <a name = "apitokens"></a>

These project needs these API tokens: 

```OPENAI_API_KEY``` - OpenAI API key which you can get here: [OpenAI API key](https://platform.openai.com/account/api-keys)

```STABLE_DIFFUSION_API_KEY``` - Stable Diffusion API key which you can get here: [Stable Diffusion API key](https://beta.dreamstudio.ai/account)

```TELEGRAM_BOT_TOKEN``` - Telegram Bot API key which you can get here after creation of your bot: [@BotFather](https://t.me/BotFather)

```CRYPTOPAY_KEY``` - Crypto Bot API key which you can get here after registration in bot (Crypto Pay - Create App): [@CryptoBot](https://t.me/CryptoBot)

## Database <a name = "database"></a>

This project requires PostgreSQL database with two tables: users(user_id, username, chatgpt, dall_e, stable_diffusion), orders(invoice_id, user_id, product) and messages(id, user_id, role, content, messages). 

Users and information about them will be added to the "users" table, orders will be added to the "orders" table and ChatGPT context window messages will be added to the "messages" table.

```DATABASE_URL``` - url to database.

## How to deploy <a name = "howtodeploy"></a>

This project was deployed on the [Railway](https://railway.app/).

For deployment you just need to create the GitHub repository, click "Start a New Project" button on the Railway website.

![image](https://user-images.githubusercontent.com/60838512/232328076-fd3f8281-e523-4b08-ade9-47cd3c7fb9ab.png)

After that you need to choose "Deploy from GitHub repo".

![image](https://user-images.githubusercontent.com/60838512/232328194-5fbfcea8-1cfd-4b4e-b484-727a3e9498be.png)

Here you need to choose your repository.

![image](https://user-images.githubusercontent.com/60838512/232328334-2db545e9-07ba-4b1b-a89a-14f0ecbbf12e.png)

After that click "add variables".

![image](https://user-images.githubusercontent.com/60838512/232328415-5d10a920-a8a6-4c11-8675-9ad5ce6fb30a.png)

Add your project's variables. For example, for this project you need to add here 4 variables: CRYPTOPAY_KEY, OPENAI_API_KEY, STABLE_DIFFUSION_API_KEY and TELEGRAM_BOT_TOKEN.

![image](https://user-images.githubusercontent.com/60838512/232328573-8cbb0eca-aca9-4fc0-8656-e303b4af90e8.png)

Return to your project and add database.

![image](https://user-images.githubusercontent.com/60838512/232328651-e02d41cc-2cd3-4b1c-ac52-a7f6312ed2cd.png)

Choose PostgreSQL.

![image](https://user-images.githubusercontent.com/60838512/232328670-25835f92-57bd-4f2b-9477-075638574454.png)

Here you need to press create tables.

![image](https://user-images.githubusercontent.com/60838512/232328709-476b146f-42e6-44ed-826f-c10762697aeb.png)

For example, tables for this project:

Table for storing users:

![image_2024-10-04_12-18-46](https://github.com/user-attachments/assets/e562ab58-d3ec-469d-b1ad-4cf3dc216635)

Table for storing orders:

![image_2024-10-04_12-19-25](https://github.com/user-attachments/assets/74133980-4aca-4460-8340-bd77f22c75d0)

Table for storing context:

![image_2024-10-04_12-17-50](https://github.com/user-attachments/assets/c803dca2-4086-4e40-a990-ce90e7866f58)

Go back to the variables and add DATABASE_URL via "Add reference". 

Also go to worker – Settings – Public network and click “Generate Domain”. Copy this domain and add it to the "BASE_WEBHOOK_URL" variable. It should be something like “https://**Your unique part**.up.railway.app/”. After that, go to Crypto Bot - Crypto Pay - My Applications - **Your Application** - Webhooks, click "Enable Webhooks" and send the URL "https://**Your unique part**.up.railway.app/**CRYPTO BOT API TOKEN**".

All variables:

![image](https://github.com/user-attachments/assets/b68b26a9-fce8-4666-a33c-aaac12ef861e)

## License <a name = "license"></a>

[License](https://github.com/vladislav-bordiug/ChatGPT_DALL_E_StableDiffusion_Telegram_Bot/blob/main/LICENSE) - this project is licensed under Apache-2.0 license.
