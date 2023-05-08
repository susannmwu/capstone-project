"use strict;"

function addEntries(evt) {
    evt.preventDefault();

    const formInputs = {
        np_name: document.querySelector("#np-field").value,
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
        document.querySelector("#entries").insertAdjacentHTML("beforeend", `<ul><li class="add-bolding">${addEntries["np"]}<br></li><li>${addEntries["entry"]}</li></ul>`);

    });
}
// i could insert a line break to resolve the reformatting of the entries
document.querySelector("#journal-entry-form").addEventListener("submit", addEntries);