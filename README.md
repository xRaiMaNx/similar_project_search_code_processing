# parse-for-similar-project

### Установка
Для работы проекта необходимо установить *preprocess*.

## Использование
Поместить в корневую папку файл формата *.csv* вида:

*"owner","name","language","stargazers_count","commit_sha","repo_id"*

Запускаем обработку:

```shell
python3 run.py
```
Рекомендуем использовать nohup:
```shell
nohup python3 -u run.py &
```

Готовые JSON файлы будут находиться в папке *jsons*.
