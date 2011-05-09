jQuery(document).ready(function() {
  jQuery("ul.plus-minus-form").each(function() {
    var ul = jQuery(this);
    var canonical = jQuery(ul.children("li")[0]);
    var canonicalChildren = canonical.children();
    canonical.hide();

    var numEntries = jQuery('<input type="hidden" name="number_entries" value="0" />');
    numEntries.insertBefore(ul);

    var addText = jQuery('<a href="#">Add Entry</a>');

    var renumberEntries = function() {
      var index = 0;
      var lis = ul.children()
      lis.each(function() {
        var li = jQuery(this);
        var liChildren = li.children()
        if (index != 0) {
          var elIndex = 0;
          canonicalChildren.each(function() {
            liChildren[elIndex].name = this.name + "_" + index;
            elIndex++;
          });
        }
        index++;
      });
    }

    var subEntry = function(li) {
      li.remove();
      if (ul.children().length == 1)  //  only the canonical remains
        addText.show();
      numEntries.val(parseInt(numEntries.val()) - 1);
      renumberEntries();
    };

    var addEntry = function(li, data) {
      addText.hide();
      numEntries.val(parseInt(numEntries.val()) + 1);
      var toAdd = canonical.clone();
      toAdd.children().each(function() {
        this.name = this.name + "_" + numEntries.val();
      });
      jQuery('<input type="button" value="-" />').click(function() { subEntry(toAdd); }).appendTo(toAdd);
      jQuery('<input type="button" value="+" />').click(function() { addEntry(toAdd); }).appendTo(toAdd);
      toAdd.insertAfter(li).show();
      renumberEntries();
    };

    addText.click(function() {
      addEntry(canonical);
    });
    addText.insertBefore(ul);
  });
});
