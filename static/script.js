function AddRows(tableid, num, users) {
  table = document.getElementById(tableid);
  if (table.style.display = "None") {
    table.style.display = "table";
  }
  for (i = 0; i < num; i++) {
    users.append_entry()
    newRow = table.rows[1].cloneNode(true);
    if (table.tBodies[0] ) {
      table.tBodies[0].appendChild(newRow);
    }
    else {
      table.appendChild(newRow);
    }
    newRow.style.display = "table-row";
  }
}

function AddUserRows(tableid, num){
    var table = document.getElementById(tableid);
    row = 0

    while (num > 0 && row < table.rows.length) {
      if (table.rows[row].style.visibility == "collapse") {
        table.rows[row].style.visibility = "";
        num = num - 1
      }
      row  = row + 1
    }
}
