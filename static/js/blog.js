$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-contact .modal-content").html("");
        $("#modal-contact").modal("show");
      },
      success: function (data) {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-contact").modal("hide");
        }
        else {
          $("#modal-contact .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create contact
  $(".js-contact").click(loadForm);
  $("#modal-contact").on("submit", ".js-blog-contact", saveForm);});
