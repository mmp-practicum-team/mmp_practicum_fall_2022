### Запуск Flask примера внутри Docker-контейнера
1. Чтобы собрать докер образ:
   ```bash
   docker build -t repo_name/image_name:image_tag .
   ```
2. Чтобы его запустить:
   ```bash
   docker run -p 5000:5000 -v "$PWD/FlaskExample/artifacts:/root/FlaskExample/artifacts" --rm -i repo_name/image_name:image_tag
   ```
