# Taqwa

## How to run
1. copy .env file to /src
2. run ```docker-compose up -d``` in root
3. if no errors, use bot here: https://t.me/taqwa_test_bot

### Docker containers:
- database: mongo image with creds in .env
- frontend: site written in react
- backend: logic of service in python
- nginx: need for proxy requests on browser between front and back

### Project structure
- frontend: ui для добавления вопроса
- src: backend часть сервиса
- taqwa: mobile
Более подробная инфа внутри readme самого компонента