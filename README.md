# audio-download-bot

# Курсовая работа по Конструированию ПО

# build & run:
1. Создаем папку для проекта
2. Открываем cmd в нашей папке
3. mkdir secrets и в этой папке создаем secret_token.txt вставляем туда свой token
4. docker build -t audio-tg-botv1 .
5. docker run -d --name telegram-bot-container audio-tg-botv1

# c4 model diagrams
1. System context diagram
   
   ![alt text](https://cdn.discordapp.com/attachments/821313543655260221/1243175750383829064/systemcontext.png?ex=66508523&is=664f33a3&hm=86e620eb81cdb04a81ae03b02a5dada2add40a9cd50ded480bf4e71c542c7ed0&)
3. Container diagram
   
   ![alt text](https://cdn.discordapp.com/attachments/821313543655260221/1243175717332713472/system.png?ex=6650851c&is=664f339c&hm=f41ffec6755140e34c3a25c0f5a8faff733f43f28aab92587f1dd79c57e9391c&)
