'use strict';

function initMap() {
    const map = new google.maps.Map(document.querySelector("#map"), {
        center: {
            lat: 72,
            lng: -140,
          },
        });
    
    const parkInfo = new google.maps.InfoWindow();

    fetch("/api/map")
        .then((response) => response.json())
        .then((coordinates) => {
            for (const coords of coordinates) {
                const parkInfoContent = `
                ${coords.np_name}`

                const parkMarker = new google.maps.Marker({
                    position: {
                        lat: coords.latitude,
                        lng: coords.longitude,
                    },
                    map: map
                
                });
                parkMarker.addListener("click", () => {
                    parkInfo.close();
                    parkInfo.setContent(parkInfoContent);
                    parkInfo.open(map, parkMarker);
                });
            }
        })

        };
        
