// Создаем карту с центром и начальным масштабом
var map = new ol.Map({
    target: "map",
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM(),
        }),
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([-99.9912, 38.8093]),
        zoom: 5,
    }),
});

// Создаем функцию стиля для меток
var markerStyleFunction = (feature) => {
    var color;

    // Определите условия для определения цвета в зависимости от данных метки
    if (feature.get("type") === "cargo") {
        color = "red";
    } else if (feature.get("type") === "car") {
        color = "blue";
    } else {
        color = "green";
    }

    return new ol.style.Style({
        image: new ol.style.Circle({
            radius: 6,
            fill: new ol.style.Fill({
                color: color,
            }),
            stroke: new ol.style.Stroke({
                color: "white",
                width: 2,
            }),
        }),
    });
};

// Создаем источник данных для меток
var source = new ol.source.Vector({
    features: [],
});

// Создаем слой меток
var layer = new ol.layer.Vector({
    source: source,
    style: markerStyleFunction,
});

// Добавляем слой на карту
map.addLayer(layer);

// Создаем всплывающее окно для отображения описания метки
var popup = new ol.Overlay({
    element: document.getElementById("popup"),
    positioning: "bottom-center",
    stopEvent: false,
});

// Добавляем всплывающее окно к карте
map.addOverlay(popup);

// Обрабатываем событие наведения на метку
map.on("pointermove", (event) => {
    var feature = map.forEachFeatureAtPixel(event.pixel, (feature) => {
        return feature;
    });

    if (feature) {
        var coordinate = event.coordinate;
        var name = feature.get("name");
        var description = feature.get("description");

        popup.setPosition(coordinate);
        popup.getElement().innerHTML =
            "<strong>" + name + "</strong><br>" + description;
        popup.getElement().style.display = "block";
    } else {
        popup.getElement().style.display = "none";
    }
});

// Функция для обновления меток на карте
function updateMarkers() {
    // Отправляем GET-запрос на сервер для получения данных

    fetch("http://0.0.0.0:8000/geo/")
        .then((response) => {
            if (!response.ok) {
                throw Error(response.status);
            }
            return response.json();
        })
        .then((data) => {
            // Очищаем источник данных от предыдущих меток

            console.log(data);
            source.clear();

            // Перебираем данные и создаем новые метки
            data.cars.forEach(function (item) {
                var lonLat = ol.proj.fromLonLat([
                    item.location.lng,
                    item.location.lat,
                ]);

                var marker = new ol.Feature({
                    geometry: new ol.geom.Point(lonLat),
                    name: item.car_number,
                    description: "car",
                    type: "car",
                });

                source.addFeature(marker);
            });

            data.cargo.forEach(function (item) {
                var lonLat = ol.proj.fromLonLat([
                    item.pick_up.lng,
                    item.pick_up.lat,
                ]);

                var marker = new ol.Feature({
                    geometry: new ol.geom.Point(lonLat),
                    name: item.id,
                    description: item.description,
                    type: "cargo",
                });

                source.addFeature(marker);
            });
        })
        .catch((err) => {
            alert(err);
        });
}

// Обновляем метки каждые 15 секунд
setInterval(updateMarkers, 5000);

// Запускаем обновление меток в первый раз
updateMarkers();
