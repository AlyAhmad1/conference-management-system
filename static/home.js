$(document).ready(()=>{
    $(".icon").click(()=>{
        $("ul").toggleClass("show");
        $("nav").toggleClass("stick");
    });
        // MDB Lightbox Init
        $(function () {
            $("#mdb-lightbox-ui").load("mdb-addons/mdb-lightbox-ui.html");
          });
})



