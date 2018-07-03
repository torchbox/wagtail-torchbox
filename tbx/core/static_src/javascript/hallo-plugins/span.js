(function() {
  (function($) {
    return $.widget("IKS.spanbutton", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Span',
          icon: 'icon-user',
          command: null
        });
        toolbar.append(button);
        button.on("click", function(event) {
            return widget.options.editable.execute('insertHTML',
                                                   '<span>' + document.getSelection() + '</span>');
        });
      }
    });
  })(jQuery);

}).call(this);
