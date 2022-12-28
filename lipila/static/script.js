// function to add a spinner to the button element
$(document).ready(function(){
  $("button").click(function(){
    $("button").addClass('spin');
    $("button").disabled = true;
    $("button").form.firstElementChild.disabled = true;

    window.setTimeout(function() {
        $("button").removeClass('spin');
        $("button").disabled = false;
        $("button").form.firstElementChild.disabled = false;
    }, 4000)
  });
});

// Function to search for student by names
function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
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