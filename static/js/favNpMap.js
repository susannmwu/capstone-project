'use strict';

function initMap() {
    const map = new google.maps.Map(document.querySelector("#map"), {
        center: {
            lat: 37.0902,
            lng: -95.7129,
          },
        zoom: 4
        });
    
    const parkInfo = new google.maps.InfoWindow();
    // need a list of markers 
    // inside the fetch, we would need to go through the coordinates and append to 
    // list of markers
    fetch("/api/map")
        .then((response) => response.json())
        .then((coordinates) => {
            for (const coords of coordinates) {
                const parkInfoContent = `
                <li>${coords.np}</li>`;

                const parkMarker = new google.maps.Marker({
                    position: {
                        lat: coords.latitude,
                        lng: coords.longitude,
                    },

                    map: map,
                    
                });
                    
                parkMarker.addListener("click", () => {
                    parkInfo.close();
                    parkInfo.setContent(parkInfoContent);
                    parkInfo.open(map, parkMarker);
                });
            }
        })

        };
       
