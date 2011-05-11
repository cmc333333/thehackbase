function createPlusMinus(root, prefix) {
  if (!prefix)
    prefix = "form";
  jQuery(root).each(function() {
    var ul = jQuery(this);
    var canonical = jQuery(ul.children("li")[0]);
    var canonicalChildren = canonical.find('input, textarea, select, label');
    canonical.hide();

    var numEntries = jQuery('#id_' + prefix + '-TOTAL_FORMS');

    var addText = jQuery('<a href="#">Add Entry</a>');

    var renumberEntries = function() {
      var index = 0;
      var lis = ul.children()
      lis.each(function() {
        var li = jQuery(this);
        var liChildren = li.find('input, textarea, select, label')
        if (index != 0) {
          var elIndex = 0;
          canonicalChildren.each(function() {
            var child = jQuery(this)
            if (child.attr('for'))
              jQuery(liChildren[elIndex]).attr('for', child.attr('for').replace('__prefix__', index));
            if (child.attr('name'))
              jQuery(liChildren[elIndex]).attr('name', child.attr('name').replace('__prefix__', index));
            if (child.attr('id'))
              jQuery(liChildren[elIndex]).attr('id', child.attr('id').replace('__prefix__', index));
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
      toAdd.find('input, textarea, select').each(function() {
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
}
