const actorSelectorBtn = document.querySelector("[data-actor-selector-btn]");
const actorsField = document.querySelector("[data-actors]");
const actorSelectorInput = document.querySelector(
  ".modal .actor-selector-input"
);
const modal = document.querySelector("#actor-selector-modal");
const actorsDiv = document.querySelector(".modal .actors-div");

modal.addEventListener("shown.bs.modal", () => {
  actorSelectorInput.focus();
});

// const actors = actorsField.value.split(",");
const actors = [
  "Ariana Grande",
  "Kylie Jenner",
  "Kendall Jenner",
  "Kim Kardashian",
];
const ul = document.createElement("ul");
ul.className = `actors mb-2 list-group ${
  actors.length > 0 ? "d-block" : "d-none"
}`;

actors.forEach((actor) => {
  const li = document.createElement("li");
  const button = document.createElement("button");
  button.className = "delete-actor";
  button.innerHTML = "&times;";
  li.innerText = actor;
  li.className = "mb-2";
  li.appendChild(button);
  ul.appendChild(li);
});
actorsDiv.appendChild(ul);
