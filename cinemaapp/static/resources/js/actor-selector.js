const actorSelectorBtn = document.querySelector("[data-actor-selector-btn]");
/**@var HTMLSelectElement actorsField  */
const actorsField = document.querySelector("[data-actors]");
const actorSelectorInput = document.querySelector(
  ".modal .actor-selector-input"
);
const modal = document.querySelector("#actor-selector-modal");
const actorsDiv = document.querySelector(".modal .actors-div");
const selectedActorsDiv = document.querySelector(
  ".selected-actors-list .actor-list"
);

modal.addEventListener("shown.bs.modal", () => {
  actorSelectorInput.focus();
});

actorsField.addEventListener("change", updateActorsList);

function updateActorsList() {
  console.log('something changed');
  actors = document.querySelectorAll("[data-actors] option[selected]");
  selectedActorsDiv.innerHTML = "";
  actorsDiv.innerHTML = "";
  actors.forEach((actor, index) => {
    const div = document.createElement("div");
    div.className = "d-inline-block p-2 bg-light";
    const button = document.createElement("button");
    button.className = "delete-actor";
    button.innerHTML = "&times;";
    button.dataset.index = index;
    button.addEventListener("click", removeTempActor);
    div.innerText = actor.value;
    div.className = "mb-2";
    div.appendChild(button);
    selectedActorsDiv.appendChild(div);
  });
};

actorSelectorInput.addEventListener("blur", (event) => {
  event.target.value = "";
  document.querySelector('ul.auto-complete-list').innerHTML = ''
})

actorSelectorInput.onkeyup = async (event) => {
  const url = `/search-actors/?actor=${event.target.value}`;
  const ul = document.querySelector('ul.auto-complete-list')
  ul.innerHTML = ''
  let liContents = `
  <form method="post" action="/add-actor/">
    <input type="hidden" name="actor" value="${event.target.value}">
    <button class="p-0 m-0 border-0"> <i class="fas fa-plus-circle"></i> Add this actor <b>${event.target.value}</b> </button>
  </form>
    `
  await axios
    .get(url)
    .then((response) => {
      if (response.data.length > 0) {
        response.data.forEach((row, index = 0) => {
          if (index === 0) {
            addLi(ul, liContents)
          }
          addLi(ul, row.name, `/add-actor/?actor=${row.name}`)
        })
      } else {
        addLi(ul, liContents)
      }
    })
    .catch((err) => console.warn(err));
};

// a function to add a li element on a ul element
function addLi(ul, content, link = null) {
  const li = document.createElement("li");
  if (link) {
    li.innerHTML = `<a href="#" class="d-block selectAnActor">${content}</a>`
    li.querySelector('a').addEventListener('click', selectActor)
  } else {
    li.innerHTML = content
  }
  ul.appendChild(li);
}

function selectActor(e) {
  e.preventDefault();
  const actor = e.target.innerText;
  const option = document.createElement("option");
  option.value = actor;
  option.innerText = actor;
  option.selected = true;
  actorsField.appendChild(option);
  updateActorsList();

}

// const actors = actorsField.value.split(",");
let actors = document.querySelectorAll("[data-actors] option[selected]");

const ul = document.createElement("ul");
ul.className = `actors mb-2 list-group ${actors.length > 0 ? "d-block" : "d-none"
  }`;
console.log(actors);

actors.forEach((actor, i) => {
  const li = document.createElement("li");
  const button = document.createElement("button");
  button.className = "delete-actor";
  button.innerHTML = "&times;";
  button.dataset.index = i;
  button.addEventListener("click", removeTempActor);
  li.innerText = actor.value;
  li.className = "mb-2";
  li.appendChild(button);
  ul.appendChild(li);
});
actorsDiv.appendChild(ul);

function removeTempActor(event) {
  actorsField.remove(event.target.dataset.index);
  this.parentElement.remove();
  updateActorsList();
}
