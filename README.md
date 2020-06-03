# Запуск
Создать каталог images
Вколотить в консоль:

    export FLASK_ENV=development
    export FLASK_APP="src/app:create_app"
    flask run

# Что реализовано
* POST /auth/login
* POST /auth/logout
* POST /users
* GET /users/\<id\>
* GET /ads (не до конца)
* GET /users/\<id\>/ads (не до конца)
* POST /ads (не до конца)
* POST /users/\<id\>/ads (не до конца)
* GET /ads/\<id\> (не до конца)
* DELETE /ads/\<id\>
* GET /cities
* POST /cities
* GET /colors
* POST /colors
* POST /images (какие-то траблы с кавычками в названии файла)
* GET /images/\<name\>