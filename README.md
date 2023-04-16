# ChatGPT, DALL·E, Stable Diffusion Telegram bot
## About
Nowadays neural networks are able to conduct a dialogue, quickly search for the information we need, answer questions, explain complex concepts and draw pictures according to words. This is Telegram bot written in Python that allows to chat with ChatGPT and generate images using DALL·E and Stable Diffusion. I think it is very comfortable to unite these neural networks in one Telegram bot.

You can look on this bot in Telegram: [@ChatGpt_Dall_E_Bot](https://t.me/ChatGPT_Dall_E_Bot)

## Start
When the user enters the start command, the bot sends him a welcome message stating that the user has free 3000 ChatGPT tokens, 3 DALL·E image generations and 3 Stable Diffusion image generations and displays 4 buttons: "💭Chatting — ChatGPT 3.5 Turbo", "🌄Image generation — DALL·E", "🌅Image generation — Stable Diffusion" and "👤My account | 💰Buy". If the user is already registered, the bot only displays buttons.

![ChatGPT, DALL·E, Stable Diffusion _ Telegram bot 2023-04-16 18-14-35 _online-video-cutter com_](https://user-images.githubusercontent.com/60838512/232325199-508eb8c5-4bfc-44ad-afde-d87b820fc4bb.gif)


## ChatGPT
If the user wants to chat with ChatGPT, he presses the "💭Chatting — ChatGPT 3.5 Turbo" button and chats.

![ChatGPT, DALL·E, Stable Diffusion _ Telegram bot 2023-04-16 18-34-00 _online-video-cutter com_](https://user-images.githubusercontent.com/60838512/232324085-8998d1e4-c075-4b72-818f-e516838c199a.gif)

## DALL·E
If the user wants to generate image with DALL·E, he presses the "🌄Image generation — DALL·E" button and generates.

![ChatGPT, DALL·E, Stable Diffusion _ Telegram bot – _1_ 2023-04-16 18-47-44 _online-video-cutter com_ (1)](https://user-images.githubusercontent.com/60838512/232324731-81761500-1a5c-4bd3-a728-b8917c8dd1eb.gif)

Generated image:

<img src="https://user-images.githubusercontent.com/60838512/232324828-8d4d1f50-20cd-412b-bb01-ae975a771361.png" width="512" height="512">

## Stable Diffusion
If the user wants to generate image with Stable Diffusion, he presses the "🌅Image generation — Stable Diffusion" button and generates.

![ChatGPT, DALL·E, Stable Diffusion _ Telegram bot 2023-04-16 19-06-33 _online-video-cutter com_](https://user-images.githubusercontent.com/60838512/232325734-ac97a733-91ef-490e-a30f-e970358ad585.gif)

Generated image:

![image](https://user-images.githubusercontent.com/60838512/232325586-649bb911-aa0a-4a7b-9fa1-4ea544f93485.png)

## Account and buy
If the user wants to see account information or buy tokens and generations, he presses the "👤My account | 💰Buy" button. After pressing the button, the bot displays information about the rest of the user's ChatGPT tokens, DALL·E image generations and Stable Diffusion image generations. If user wants to buy tokens and generations, he presses "💰Buy tokens and generations" button, selects product and currrency. After that, the user needs to press the "💰Buy" button and pay in Crypto Bot if he wants to pay. If the user has paid, he should press "☑️Check" button and tokens or image generations will be added to his account. If the user hasn't paid, the bot will display the message "⌚️We have not received payment yet".

![ChatGPT, DALL·E, Stable Diffusion _ Telegram bot 2023-04-16 19-14-29 _online-video-cutter com_](https://user-images.githubusercontent.com/60838512/232326500-dc77b158-bb4f-49b9-a7c3-f9198ae56bfb.gif)

## API tokens

These project needs these API tokens: 

```CHAT_GPT3_API_KEY``` - OpenAI API key which you can get here: [OpenAI API key](https://platform.openai.com/account/api-keys)

```STABLE_DIFFUSION_API_KEY``` - Stable Diffusion API key which you can get here: [Stable Diffusion API key](https://beta.dreamstudio.ai/account)

```TELEGRAM_BOT_TOKEN``` - Telegram Bot API key which you can get here after creation of your bot: [@BotFather](https://t.me/BotFather)

```CRYPTOPAY_KEY``` - Crypto Bot API key which you can get here after registration in bot (Crypto Pay - Create App): [@CryptoBot](https://t.me/CryptoBot)

## Database

These project requires PostgreSQL database with two tables: orders(purchase_id, user_id) and users(user_id, username, chatgpt, dall_e, stable_diffusion). 

Users and information about them will be added to the "users" table, orders would be added to the "orders" table.

```DATABASE_URL``` - url to database.

## How to deploy

This project was deployed on the [Railway](https://railway.app/).

For deployment you just need to create the GitHub repository, click "Start a New Project" button on the Railway website.

![image](https://user-images.githubusercontent.com/60838512/232328076-fd3f8281-e523-4b08-ade9-47cd3c7fb9ab.png)

After that you need to choose "Deploy from GitHub repo".

![image](https://user-images.githubusercontent.com/60838512/232328194-5fbfcea8-1cfd-4b4e-b484-727a3e9498be.png)

Here you need to choose your repository.

![image](https://user-images.githubusercontent.com/60838512/232328334-2db545e9-07ba-4b1b-a89a-14f0ecbbf12e.png)

After that click "add variables".

![image](https://user-images.githubusercontent.com/60838512/232328415-5d10a920-a8a6-4c11-8675-9ad5ce6fb30a.png)

Add your ptoject's variables. For example, for this project you need to add 4 variables: CHAT_GPT3_API_KEY, CRYPTOPAY_KEY, DATABASE_URL, STABLE_DIFFUSION_API_KEY and TELEGRAM_BOT_TOKEN.

![image](https://user-images.githubusercontent.com/60838512/232328573-8cbb0eca-aca9-4fc0-8656-e303b4af90e8.png)

Return to your project and add database.

![image](https://user-images.githubusercontent.com/60838512/232328651-e02d41cc-2cd3-4b1c-ac52-a7f6312ed2cd.png)

Choose PostgreSQL.

![image](https://user-images.githubusercontent.com/60838512/232328670-25835f92-57bd-4f2b-9477-075638574454.png)

Here you need to press create tables.

![image](https://user-images.githubusercontent.com/60838512/232328709-476b146f-42e6-44ed-826f-c10762697aeb.png)

For example, tables for these projects:

![image](https://user-images.githubusercontent.com/60838512/232328867-a2c7237a-36da-4b0f-bc1f-7b55ab55832c.png)

![image](https://user-images.githubusercontent.com/60838512/232328899-2a0dd7de-932e-45c8-8580-06e3a281fb7a.png)

Return to variables and add DATABASE_URL. All variables:

![image](https://user-images.githubusercontent.com/60838512/232329016-5961b459-e1ca-4e73-90af-7c6dddf9d24d.png)

## License

[License](https://github.com/vladislav-bordiug/ChatGPT_DALL_E_StableDiffusion_Telegram_Bot/blob/main/LICENSE) - this project is licensed under Apache-2.0 license.
