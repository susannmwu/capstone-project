"use strict;"

const addPark = document.querySelector("#add-park");
const addToList = () => {document.querySelector("#list").insertAdjacentHTML("beforeend", "")};
addPark.addEventListener("click", addToList);


const addToTrailList = () => {document.querySelector("fav-trails-list").insertAdjacentHTML("beforeend", "")};
favListAdderButton.addEventListener("click", addToTrailList);