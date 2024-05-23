# audio-download-bot


# build & run:
1. Создаем папку для проекта
2. Открываем cmd в нашей папке
3. mkdir secrets и в этой папке создаем secret_token.txt вставляем туда свой token
4. docker build -t audio-tg-botv1 .
5. docker run -d --name telegram-bot-container audio-tg-botv1
