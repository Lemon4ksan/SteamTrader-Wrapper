# Исключения

### `SteamTraderError`
> Базовый класс, представляющий исключения общего характера.

### `UnsupportedAppID`
> Класс исключения, вызываемый в случае использования неподдерживаемого AppID.

### `ClientError`
> Класс исключения, вызываемый в случае ошибки с клиентом.

### `Unauthorized`
> Класс исключения, вызываемый в случае, если клиент не зарегистрирован.

### `AuthenticatorError`
> Класс исключения, вызываемый в случае, если мобильный аутентификатор не поключён, или не прошло 7 ней с момента его активации.

### `TradeError`
> Базовый класс исключений, вызываемых для ошибок, связанных с обменом.

### `TradeCreationFail`
> Класс исключения, вызываемый в случае, если не удалось создать предложение обмена.

### `NoTradeLink`
> Класс исключения, вызываемый в случае, если нет ссылки на обмен.

### `NoSteamAPIKey`
> Класс исключения, вызываемый в случае, если нет ключа Steam API.

### `WrongTradeLink`
> Класс исключения, вызываемый в случае, если клиент указал ссылку для обмена от другого Steam аккаунта.

### `ExpiredTradeLink`
> Класс исключения, вызываемый в случае, если ссылка для обмена больше недействительна.

### `NoBuyOrders`
> Класс исключения, вызываемый в случае, если у клиента нет запросов на покупку.

### `TradeBlockError`
> Класс исключения, вызываемый в случае, если не включён Steam Guard или стоит блокировка обменов.

### `MissingRequiredItems`
> Класс исключения, вызываемый в случае, если в инвентаре Steam отсутствуют необходимые для передачи предметы.

### `HiddenInventory`
> Класс исключения, вызываемый в случае, если инвентарь скрыт.

### `NoTradeItems`
> Класс исключения, вызываемый в случае, если у клиента нет предметов для обмена.

### `IncorrectPrice`
> Класс исключения, вызываемый в случае, если выставленная цена ниже минимальной или больше максимальной.

### `ItemAlreadySold`
> Класс исключения, вызываемый в случае, если предмет уже выставлен на продажу.

### `NoLongerExists`
> Класс исключения, вызываемый в случае, если предмет больше не существует.

### `NotEnoughMoney`
> Класс исключения, вызываемый в случае, если на балансе недостаточно средств для совершения операции.

### `NetworkError`
> Базовый класс исключений, вызываемых для ошибок, связанных с запросами к серверу.

### `OperationFail`
> Класс представляющий исключения, вызываемый в случае, если запрос был правильным, но операция не прошла успешно.

### `UnknownItem`
> Класс исключения, вызываемый в случае, если предмет не был найден.

### `SaveFail`
> Класс исключения, вызываемый в случае, если не удалось сохранить изменённый праметр на сайте.

### `InternalError`
> Класс исключения, вызываемый в случае, если при выполнении запроса произошла неизвестая ошибка.

### `BadRequestError`
> Класс исключения, вызываемый в случае отправки неправильного запроса.

### `TooManyRequests`
> Класс исключения, вызываемый в случае отправки чрезмерно большого количества запросов на сервер.

### `NotFoundError`
> Класс исключения, вызываемый в случае ответа от сервера со статус кодом 404.
