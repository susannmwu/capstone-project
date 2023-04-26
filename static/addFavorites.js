'use strict';

const favListAdderButton = document.querySelector("#add-fav-parks");
const addToList = () => {document.querySelector("#list").insertAdjacentHTML("beforeend", "")};
favListAdderButton.addEventListener("click", addToList);
