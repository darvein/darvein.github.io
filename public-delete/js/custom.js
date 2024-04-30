$(document).on("input propertychange paste change", '.FilterSearch', function(e) {
   var value = $(this).val().toLowerCase();
   var $ul = $(this).closest('ul');
   //get all lis but not the one having search input
   var $li = $ul.find('li:gt(0)');
   //hide all lis
   $li.hide();
   $li.filter(function() {
      var text = $(this).text().toLowerCase();
      return text.indexOf(value)>=0;
   }).show();
});
