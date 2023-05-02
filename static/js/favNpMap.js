'use strict';


// function initMap() {
//   const yoseCoords = {
//     lat: 37.84883288,
//     lng: -119.5571873,
//   };

// const basicMap = new google.maps.Map(document.querySelector("#map"), {
//     center: yoseCoords,
//     zoom: 11,
// });

// const yoseMarker = new google.maps.Marker({
//     position: yoseCoords,
//     title: "Yosemite NP",
//     map: basicMap
// });

// const yoseInfo = new google.maps.InfoWindow({
//     content: "<h1>Yosemite National Park</h1>",
// });

// yoseInfo.open(basicMap, yoseMarker);

// }

// Ajax

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
                console.log(coords)

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

}