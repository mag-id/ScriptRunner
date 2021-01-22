# ScriptRunner

## Description
The final project for EPAM Autumn 2020 Python Course.

Финальный проект - запускатель скриптов на сервере с вэб-интерфейсом.

1. Приложение стартует на (удалённой) машине,
в конфигурации указана папка, в которой будут находиться
скрипты для запуска и папка с конфигурациями для этих скриптов.
Если есть скрипты без конфигов, то приложение их не трогает.

2. В конфигурации можно указать:
  * параметры для запуска
  * приоритет запуска
  * что делать, если скрипт завершится с ошибкой
  * какой скрипт запустить следующим
  (до запуска цепочки скриптов нужно проверить, что для всех есть конфигурация)

3. Форма для редактирования конфигурации скрипта.
