"use strict";

function removeParks(evt){
    evt.preventDefault(); 

    const formInputs = {
        remove_park: document.querySelector("#remove_park_field").value,
    };
    // console.log(formInputs)


    fetch("/remove-park.json", {
        method: "POST",
        body: JSON.stringify(formInputs),
        headers: {
          "Content-Type": "application/json",
        },

})
    .then (response => response.json())
    .then((removeParks) => {
       document.querySelector("#fav_park").remove(removeParks["np"])
       document.querySelector("#remove_park_field").remove(removeParks["np"])
       document.querySelector("#np_name").remove(removeParks["np"])
    });
}

document.querySelector("#park_to_remove").addEventListener("submit", removeParks);

