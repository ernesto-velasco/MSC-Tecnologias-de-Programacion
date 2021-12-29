/* 
  Author: Ernesto Velasco González
  https://www.github.com/vegonz

  Este módulo genera una tabla html con bulma css
  necesita existir un div con id: table-box, que es donde se insertara
  los parametros que recibe son:
    - data: la información en formato json
    - ignoreCols: una coleccion con el nombre de las columnas 
      del json que no deben ser incluidas ej. ['id']
    - actions: un arreglo con el nombre de las acciones y sus parametros
      ej. {'eliminar': {'params': ['id_libro']}, 'favoritos': {'params': ['id_libro']}} 
      DEBE existir una función con el mismo nombre que la accion que reciba los parametros seleccionados
      que se encargue de realizar la lógica para esa acción
*/

// * Construir una tabla html con bulma a partir de un JSON
const buildTable = (data, ignoreCols, actions) => {
  let tbox = document.querySelector("#table-box");
  console.log(data);
  if (
    !data ||
    data.length === 0 ||
    data === undefined ||
    Object.keys(data).length === 0
  ) {
    return (tbox.innerHTML =
      "Ooops! Parece que aún no hay nada para mostrar 😕");
  }
  let table = document.createElement("table");
  let cols = getCols(data, ignoreCols);
  let thead = buildHead(cols);
  let tbody = buildTBody(data, cols, actions);
  table.append(thead, tbody);
  table.classList.add("table", "is-striped", "is-hoverable", "is-fullwidth");
  tbox.appendChild(table);
};

// * Obtener el nombre de las columnas
function getCols(data, ignoreCols) {
  let cols = [];
  Object.keys(data[0]).forEach((key) => {
    if (!key.startsWith(ignoreCols)) cols.push(key);
  });
  cols.push("acciones");
  return cols;
}

// * Generar thead a partir de la columnas
function buildHead(cols) {
  let thead = document.createElement("thead");
  let tr = document.createElement("tr");

  // * columna de '#'
  let numCol = document.createElement("td");
  let abbr = document.createElement("abbr");
  abbr.title = "Número";
  abbr.innerHTML = "#";
  numCol.appendChild(abbr);
  tr.append(numCol);

  cols.forEach((col) => {
    let td = document.createElement("td");
    td.innerHTML = col.toUpperCase();
    if (col == "acciones") td.span = "3";
    tr.appendChild(td);
  });
  thead.appendChild(tr);
  return thead;
}

// * Generar tbody con el array
function buildTBody(data, cols, actions) {
  let tbody = document.createElement("tbody");
  Object.values(data).forEach((element, index) => {
    let tr = document.createElement("tr");
    let numTh = document.createElement("th");
    tr.appendChild(numTh);
    numTh.innerHTML = index + 1;
    cols.forEach((col) => {
      let td = document.createElement("td");
      if (!col.startsWith("acciones")) {
        td.innerHTML = element[col];
        tr.appendChild(td);
      }
    });
    // * Agregar acciones
    let tdActions = buildActions(actions, element.id);
    // tdEliminar.innerHTML = `<button class="button is-small is-danger is-outlined" onclick='eliminar(${element.id});'>Eliminar</button>`;
    tr.appendChild(tdActions);
    tbody.appendChild(tr);
  });
  return tbody;
}

//* Generar botones para las acciones
function buildActions(actions, id) {
  let tdActions = document.createElement("td");
  // * Default actions
  // if (actions && actions.includes("editar")) {
  //   // * EDITAR
  //   let btnEditar = document.createElement("button");
  //   btnEditar.innerText = "Editar";
  //   btnEditar.classList.add(
  //     "button",
  //     "is-small",
  //     "is-primary",
  //     "is-outlined",
  //     "mx-1",
  //     "my-1"
  //   );
  //   btnEditar.setAttribute("onclick", `editar(${id})`);
  //   tdActions.appendChild(btnEditar);
  // }
  // * ELIMINAR
  let btnEliminar = document.createElement("button");
  btnEliminar.innerText = "Eliminar";
  btnEliminar.classList.add(
    "button",
    "is-small",
    "is-danger",
    "is-outlined",
    "mx-1",
    "my-1"
  );
  btnEliminar.setAttribute("onclick", `eliminar(${id})`);
  tdActions.appendChild(btnEliminar);
  if (!actions) return tdActions;
  // * EXTRA ACTIONS
  console.log(actions);
  actions.forEach((action) => {
    let btnAction = document.createElement("button");
    btnAction.innerText = action;
    btnAction.classList.add(
      "button",
      "is-small",
      "is-outlined",
      "mx-1",
      "my-1"
    );
    if (action == "editar") btnAction.classList.add("is-primary");
    btnAction.setAttribute("onclick", `${action}(${id})`);
    tdActions.appendChild(btnAction);
  });
  //btnEliminar.addEventListener("click", eliminar(id));

  // actions.forEach((action) => {
  //   let btn = document.createElement("button");
  //   btn.innerText = key;
  //   btn.classList.add("button", "is-small", "is-outlined");
  //   btn.classList.add(action.class);
  //   btn.onclick(`key`(id));
  //   tdActions.appendChild(btn);
  // });
  return tdActions;
}
export { buildTable };
