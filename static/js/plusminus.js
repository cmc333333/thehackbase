jQuery(document).ready(function() {
  jQuery("ul.plus-minus-form").each(function() {
    var ul = jQuery(this);
    var canonical = jQuery(ul.children("li")[0]);
    canonical.hide();

    var numEntries = jQuery('<input type="hidden" name="number_entries" value="0" />');
    numEntries.insertBefore(ul);

    var addText = jQuery('<a href="#">Add Entry</a>');

    var subEntry = function(li) {
      li.remove();
      if (ul.children().length == 1)  //  only the canonical remains
        addText.show();
    };

    var addEntry = function(data) {
      addText.hide();
      var index = parseInt(numEntries.val()) + 1;
      numEntries.val(index);
      var toAdd = canonical.clone();
      toAdd.children().each(function() {
        this.name = this.name + "_" + numEntries.val();
      });
      jQuery('<input type="button" value="-" />').click(function() { subEntry(toAdd); }).appendTo(toAdd);
      jQuery('<input type="button" value="+" />').click(function() { addEntry(); }).appendTo(toAdd);
      toAdd.appendTo(ul).show();
    };

    addText.click(function() {
      addEntry();
    });
    addText.insertBefore(ul);
  });
});
