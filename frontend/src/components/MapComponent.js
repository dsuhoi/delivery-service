import React, { useEffect, useRef } from "react";
import "ol/ol.css";
import "./MapComponent.css";
import { fromLonLat } from "ol/proj";
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Circle as CircleStyle, Fill, Stroke, Style } from "ol/style";
import Overlay from "ol/Overlay";
import { ApolloClient, InMemoryCache, gql } from "@apollo/client";

const MapComponent = () => {
    const mapRef = useRef(null);
    const popupRef = useRef(null);

    useEffect(() => {
        const map = new Map({
            target: mapRef.current,
            layers: [
                new TileLayer({
                    source: new OSM(),
                }),
            ],
            view: new View({
                projection: "EPSG:3857",
                center: fromLonLat([-99.9912, 38.8093]),
                zoom: 5,
            }),
        });

        const source = new VectorSource({ features: [] });

        const markerStyleFunction = (feature) => {
            const color = feature.get("color");
            return new Style({
                image: new CircleStyle({
                    radius: 5,
                    fill: new Fill({ color }),
                    stroke: new Stroke({
                        color: "white",
                        width: 2,
                    }),
                }),
            });
        };

        const layer = new VectorLayer({
            source: source,
            style: markerStyleFunction,
        });

        map.addLayer(layer);

        const popup = new Overlay({
            element: popupRef.current,
            positioning: "bottom-center",
            stopEvent: false,
        });

        map.addOverlay(popup);

        map.on("pointermove", (event) => {
            const feature = map.forEachFeatureAtPixel(
                event.pixel,
                (feature) => feature,
            );
            if (feature) {
                const coordinate = event.coordinate;
                const name = feature.get("name");
                const description = feature.get("description");

                popup.setPosition(coordinate);
                popup.getElement().innerHTML = `<strong>${name}</strong><br>${description}`;
                popup.getElement().style.display = "block";
            } else {
                popup.getElement().style.display = "none";
            }
        });

        const client = new ApolloClient({
            uri: "/api/graphql",
            cache: new InMemoryCache(),
        });

        const fetchData = async () => {
            const GET_LOCATIONS = gql`
                {
                    cargo {
                        id
                        description
                        pickUpLoc {
                            lat
                            lng
                        }
                    }
                    cars {
                        carNumber
                        loc {
                            lat
                            lng
                        }
                    }
                }
            `;
            client.query({ query: GET_LOCATIONS }).then((response) => {
                const data = response.data;
                source.clear();
                data.cars.forEach((item) => {
                    const marker = new Feature({
                        geometry: new Point(
                            fromLonLat([item.loc.lng, item.loc.lat]),
                        ),
                        name: item.carNumber,
                        description: "car",
                        color: "blue",
                    });
                    marker.setStyle(markerStyleFunction(marker));
                    source.addFeature(marker);
                });

                data.cargo.forEach((item) => {
                    const marker = new Feature({
                        geometry: new Point(
                            fromLonLat([
                                item.pickUpLoc.lng,
                                item.pickUpLoc.lat,
                            ]),
                        ),
                        name: item.id,
                        description: item.description,
                        color: "red",
                    });
                    marker.setStyle(markerStyleFunction(marker));
                    source.addFeature(marker);
                });
            });
        };

        fetchData();
        const intervalId = setInterval(fetchData, 20000);

        return () => {
            clearInterval(intervalId);
            map.setTarget(null);
        };
    }, []);

    return (
        <div>
            <div ref={mapRef} style={{ width: "100%", height: "100%" }}></div>
            <div ref={popupRef} className="ol-popup">
                <a href="/#" className="ol-popup-closer">
                    {" "}
                </a>
                <div id="popup-content"></div>
            </div>
        </div>
    );
};

export default MapComponent;
