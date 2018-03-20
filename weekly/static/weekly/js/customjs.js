$(document).ready(function(){
  // Fix the nav panel
  $(document).scroll(function() {
    var curr_scroll = $(document).scrollTop();
    if ($(document).scrollTop() > 100){
      $("#side_nav").removeClass("nav_block")
      $("#side_nav").addClass("nav_block_fix")
    }else{
      $("#side_nav").removeClass("nav_block_fix")
      $("#side_nav").addClass("nav_block")
    };
  });
});
