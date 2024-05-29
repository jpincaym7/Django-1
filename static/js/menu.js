// Cerrar el menú cuando se hace clic en un enlace
$(document).ready(function() {
    $('#menu a').on('click', function() {
      $('#menu-toggle').prop('checked', false);
    });
  });