# CareerLens-datacollector
Data collector server for CareerLens app

## Принцип работы

Этот Python-сервис работает в ответ на внешние сигналы или уведомления. После получения сигнала сервис выполняет одно из двух основных действий:

1. **Запрос данных с hh.ru.** Если сигнал указывает на необходимость получения новых данных, сервис отправляет запрос к API hh.ru, получает данные о вакансиях и сохраняет их в базу данных.

1. **Фильтрация данных из базы данных.** В случае если сигнал требует фильтрации данных, сервис извлекает нефильтрованные данные из базы данных, обрабатывает их согласно критериям, указанным в сообщении, и возвращает результат. Результатом может быть название новой коллекции в базе данных или идентификаторы добавленных записей.

Этот сервис обеспечивает динамическое получение и фильтрацию данных в зависимости от поступающих сигналов.

## Сигналы принимающее приложение

Приложение принимает json сообщение, в котором ищет два ключа:
1. "collectData" - содержит ключи page(Integer) и per_page(Integer). В последствии начинает сбор даннхых с hh.ru
2. "filterData" - **В процессе разработки**