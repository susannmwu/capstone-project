"use strict;"

function addEntries(evt) {
    evt.preventDefault();

    const formInputs = {
        park_entries: document.querySelector("#entry-field").value, 
    };

    fetch("/np-entry.json", {
        method: "POST",
        body: JSON.stringify(formInputs),
        headers: {
          "Content-Type": "application/json",
        },
    })

    .then(response => response.json())
    .then((addEntries) => {
        document.querySelector("#entries").insertAdjacentHTML("beforeend", addEntries["entry"]);
    });
}

document.querySelector("#journal-entry-form").addEventListener("submit", addEntries);