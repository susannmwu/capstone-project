"use strict;"

const removePark = document.querySelector("#add-park");
const removeFromList = () => (document.querySelector("#list").remove());
removePark.addEventListener("click", removeFromList);