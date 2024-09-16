
## Установка и запуск 
1. Клонировать проект
```
git clone https://github.com/ivangol739/clientsdb
```     
2. Перейти в каталог проекта
```
cd clientsdb
```  
3. Создать и активировать виртуальное окружение

**Windows**
```
python -m venv venv
venv\Scripts\activate
```  
**macOS и Linux**
```
python3 -m venv venv
source venv/bin/activate
```
4. Установить зависимости
```
pip install -r requirements.txt
```  
5. Настройка переменных окружения. Создать файл `.env` в корневом каталоге и добавить токены.
```
user=логин от бд
password=пароль от бд
database=название бд
```  
6. Создать БД
```  
createdb -U postgres dbclients
```  
7. Запустить проект
```
python main.ru
```  