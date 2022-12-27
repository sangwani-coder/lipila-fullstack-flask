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
