# delivery-service
>Сервис поиска ближайших машин для перевозки грузов.
<img src="docs/images/main_page.jpg" width=800>

---
### Установка
В корневой директории  выполните команду:
```sh
docker compose up -d --built
```

### Просмотр
Перейдите по адресу `0.0.0.0:8083` для просмотра карты с грузами и машинами или `0.0.0.0:8001` для работы с API сервиса.

### Архитектура
```mermaid
flowchart LR
    subgraph server [Server]
        direction TB

        subgraph db [Databases]
            direction TB
            db1[(PostGis)]
        end
        db1 <--> b1
        subgraph b1 [Backend]
            direction LR
            b2[[Cars API]]
            b3[[Cargo API]]
        end

        ng{{Nginx}} <--> b1
        react[[ReactJS]]
        ng <-- GraphQL --> react
    end

    subgraph cls [Clients]
        direction LR
        cl1([Client 1])
        cl2([Client 2])
    end
    react <-. WEB .-> cls
    ng <-. REST API .-> cls
```
Сервис разделен на три части:
- База данных PostGis
- Backend на FastAPI
- Frontend на ReactJS

### License
Copyright © 2023 [dsuhoi](https://github.com/dsuhoi).

This project is [MIT](https://github.com/dsuhoi/delivery-service/blob/main/LICENSE) licensed.
