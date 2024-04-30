$(document).ready(function() {
  let backend = 'http://backend.default.local:31002'
  let localCounter = 0;

  // Load initial server count
  $.get(backend + "/report", function(data) {
    $("#server-counter").text(data.count);
  });

  // Increment local counter when image is clicked
  $("#clickable-image").click(function() {
    localCounter++;
    $("#local-counter").text(localCounter);
  });

  // Save local counter to server when button is clicked
  $("#save-button").click(function() {
    $.get(`${backend}/click?value=${localCounter}`, function(data) {
      if (data.message === 'Successfully incremented clicked') {
        // Update server count
        $.get(backend + "/report", function(data) {
          $("#server-counter").text(data.count);
        });
      }
    });
  });
});
