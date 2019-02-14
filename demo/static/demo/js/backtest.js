$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    var formb = $('#full_form');
    console.log('Hi Ajax');
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      data: formb.serialize(),
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html("");
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    console.log('By Ajax');
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
          console.log(data.backtest_details);
          if (typeof(Storage) !== "undefined") {
            // Store
            // https://stackoverflow.com/q/6193574/5176549
            sessionStorage.setItem("backtest_details", JSON.stringify(data.backtest_details));
            console.log(sessionStorage.getItem('backtest_details'))
          }
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var saveBacktest = function () {
    var strategy_details = $('#id_backtest_details');
    try {
      var data=sessionStorage.getItem('backtest_details');
      $('#id_backtest_details').val(data)
    }
    catch(err) {
        console.log('Still not data passed');
    }
  };



  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

  //Modification of the backtest_details
  // https://stackoverflow.com/questions/44087655/edit-form-field-value-on-template
  $(".js-create-backtest").click(saveBacktest);

});
