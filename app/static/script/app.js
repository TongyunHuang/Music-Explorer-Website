const newBg = "lightcyan";
const oldBg = "#eee";
const allTablesId = ["songTable", "artistTable", "coverTable", "commentTable", "albumTable"]
var dataTable;
var genreFilter = [];

function receive(dataVariable) {
    dataTable = dataVariable;
}

function updateTableOnClick(id) {
    let a = document.getElementById(id);
    if (a.style.background == newBg) {
        a.style.background = oldBg;
    } else {
        allTablesId.forEach(function(items, index) {
            let tempTable = document.getElementById(items);
            console.log(tempTable.style.background)
            if (tempTable.style.background == newBg) {
                tempTable.style.background = oldBg;
            }
        });
        if (a.innerHTML !== "Reset Tables") {
            a.style.background = newBg;
        }
        updateTable(document.getElementById(id).innerHTML);
    }
}

function updateTable(tableName) {
    var tableTitle = document.getElementById("table_title");
    var tableBody = document.getElementById("table_entry");
    if (tableName === "Reset Tables") {
        tableBody.innerHTML = "";
        tableTitle.innerHTML = "";
        return;
    }
    tableTitle.innerHTML = "";
    var title = ``;
    if (tableName === "Song") {
        var col = dataTable["songCol"];
        col.forEach(function(items, index) {
            title += `<th>${items}</th>\n`;
        });
    } else if (tableName === "Album") {
        var col = dataTable["albumCol"];
        col.forEach(function(items, index) {
            title += `<th>${items}</th>\n`;
        });
    } else if (tableName === "Cover") {
        var col = dataTable["coverCol"];
        col.forEach(function(items, index) {
            title += `<th>${items}</th>\n`;
        });
    } else if (tableName === "Comment") {
        var col = dataTable["commentCol"];
        col.forEach(function(items, index) {
            title += `<th>${items}</th>\n`;
        });
    } else if (tableName === "Artist") {
        var col = dataTable["artistCol"];
        col.forEach(function(items, index) {
            title += `<th>${items}</th>\n`;
        });
    }
    tableTitle.innerHTML = title;

    tableBody.innerHTML = "";
    var tableEntry = dataTable[tableName];
    var row = ``;
    tableEntry.forEach(function(items, index) {
        row += `<tr>\n`
        items.forEach(function(entry, i) {
            row += `    <td>${entry}</td>\n`
        })
        row += `</tr>\n`
    });
    tableBody.innerHTML += row;
}

function insertCRUD() {
    var tableUpdated;
    for (var i = 0; i < allTablesId.length; i++) {
        let t = document.getElementById(allTablesId[i]);
        if (t.style.background == newBg) {
            tableUpdated = allTablesId[i];
            break;
        }
    }
    if (tableUpdated != null) {
        var updateModal = document.getElementById("insertModal");
        updateModal.style.display = 'flex';
        var infoCRUD = document.getElementById("infoCRUD");
        infoCRUD.innerHTML = `You are <span style="color: blue">INSERTING</span> new data <span style="color: blue">INTO</span> `;
        infoCRUD.innerHTML += `<span style="color: Red">${document.getElementById(tableUpdated).innerHTML}</span>`;
        infoCRUD.innerHTML += " table";

        var form = document.getElementById("modalInput");
        var tableCol = dataTable[document.getElementById(tableUpdated).innerHTML.toLowerCase() + "Col"]
        form.innerHTML = "";
        tableCol.forEach(function(items, index){
            var res = ``;
            res += `<label class="modalLabel">${items}:</label>`;
            res += `<input class="modalInputForm" type="text" placeholder="Enter ${items} here">`;
            form.innerHTML += res;
        });
    }
}

function updateCRUD() {
    var tableUpdated;
    for (var i = 0; i < allTablesId.length; i++) {
        let t = document.getElementById(allTablesId[i]);
        if (t.style.background === newBg) {
            tableUpdated = allTablesId[i];
            break;
        }
    }
    if (tableUpdated != null) {
        var updateModal = document.getElementById("updateModal");
        updateModal.style.display = 'flex';
        var infoCRUD = document.getElementById("infoCRUD");
        infoCRUD.innerHTML = "You are UPDATING ";
        infoCRUD.innerHTML += document.getElementById(tableUpdated).innerHTML;
        infoCRUD.innerHTML += " table";
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'none';
}


function uplift() {
    let a = document.getElementById("td_uplifting");
    updateOnClick(a);
}

function relax() {
    let a = document.getElementById("td_relaxing");
    updateOnClick(a);
}

function sad() {
    let a = document.getElementById("td_sad");
    updateOnClick(a);
}



function search() {
    let input = document.getElementById("searchInput");
    
    input = input.value.toLowerCase();
    let tableBody = document.getElementById("table_entry");
    for (var i = 0, row; row = tableBody.rows[i]; i++) {
        let title = row.cells[0];
        console.log(title);
        title = title.textContent.toLowerCase();
        if (!title.includes(input)) {
            row.style.display = "none";
        } else {
            row.style.display = "";
        }
    }
}