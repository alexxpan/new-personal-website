// JS for collapsible navigation items
var collapsibles = document.getElementsByClassName("collapsible");

// Add onClick event for each collapsible
for (var i = 0; i < collapsibles.length; i++) {
    collapsibles[i].addEventListener("click", function() {
    var content = this.nextElementSibling;
    // Toggle content between 0 and max height when clicked
    if (parseInt(content.style.maxHeight) > 0){
        content.style.maxHeight = 0;
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
        // Scroll to the top of the clicked collapsible
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#contact").offset().top
        }, 500);

    } 
  });
}