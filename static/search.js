const itemSearch = (item) =>{
    var filter, table, tr, td, i, txtValue;
    filter = item.toUpperCase();
    table = document.getElementById("corptable");
 
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];       
        if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
        }       
    }
}


const Search = (item) =>{
    var filter, table, tr1, td, i, txtValue;
    filter = item.toUpperCase();
    table = document.getElementsByClassName("table")["0"];
   
    tr1 = table.getElementsByTagName("tr");
    for (i = 0; i < tr1.length; i++) {
        td = tr1[i].getElementsByTagName("td")[1];       
        if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr1[i].style.display = "";
        } else {
            tr1[i].style.display = "none";
        }
        }       
    }
}