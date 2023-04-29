"use strict;"

const favListAdderButton = document.querySelector("#add-fav-parks");
const addToList = () => {document.querySelector("#list").insertAdjacentHTML("beforeend", "")};
favListAdderButton.addEventListener("click", addToList);


const addToTrailList = () => {document.querySelector("fav-trails-list").insertAdjacentHTML("beforeend", "")};
favListAdderButton.addEventListener("click", addToTrailList);