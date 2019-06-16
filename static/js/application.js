var socket;

var settings = new Object();

function send_settings() {
    data = JSON.stringify(settings);
    console.log("Sending settings with data = " + data);
    $.get('http://' + document.domain + ':' + location.port + '/settings/'+data, function(data, status){
    // alert("Data: " + data + "\nStatus: " + status);
  });
}
// function send_settings_no_of_bands(data){
//     console.log("Sending settings with data = " + data);
//     $.get('http://' + document.domain + ':' + location.port + '/settings_no_of_bands/'+data, function(data, status){
//     // alert("Data: " + data + "\nStatus: " + status);
//   });
// }


function initSettings() {
  settings.cnn = false;
  settings.lstm = true;
  settings.band = 1;
  // default values ....
}

// function set_bands_one() {
//   var settingObject_bands = new Object();
//   settingObject_bands.one = false;
//   settingObject_bands = true;
//   send_settings(JSON.stringify(settingObject));
// }

// function set_model_lstm() {
//   var settingObject = new Object();
//   settingObject.cnn = false;
//   settingObject.lstm = true;
//   send_settings(JSON.stringify(settingObject));
// }

// function set_model_lstm() {
//   var settingObject = new Object();
//   settingObject.cnn = false;
//   settingObject.lstm = true;
//   send_settings(JSON.stringify(settingObject));
// }

function set_model_cnn() {
  // var settingObject = new Object();
  settings.cnn = true;
  settings.lstm = false;
  send_settings();
}

function set_model_lstm() {
  // var settingObject = new Object();
  settings.cnn = false;
  settings.lstm = true;
  send_settings();
}

$(document).ready(function(){
    //connect to the socket server.
     
    var str1 = "data:image/png;base64,";
    initSettings();

    $("#start").prop('disabled', false);
    $("#stop").prop('disabled', true);

    //receive details from server
  $('#start').on('click',function(){
        $("#start").prop('disabled', true);
        $("#stop").prop('disabled', false);
        socket=io.connect('http://' + document.domain + ':' + location.port + '/test');
        socket.connect();
        socket.on('newnumber', function(msg) {
            console.log("received");
            
            $.ajax({url: "get_image", success: function(result){
                $('#div_img').html("");
                $('#div_img').html('<img class="img-responsive" style="width:100%;" src="data:image/png;base64,' + result + '" />');
            }});
            
        });
  }); 

  $("#settings input[name='model_type']").click(function(){
    model = $('input:radio[name=model_type]:checked').val();
    console.log("You selected model_type = " + model);
    if(model == "cnn") {
      set_model_cnn();
    } else if(model == "lstm") {
      set_model_lstm();
    }
  });



  


  $('#band_selector').on('change',function() {
    selectedBand = $("#band_selector").val();
    console.log(selectedBand);
    if(selectedBand != -1) {
      // do something something
      settings.band = selectedBand;
      send_settings();
    }
  });





  $('#stop').on('click',function(){
        $("#start").prop('disabled', false);
        $("#stop").prop('disabled', true);
        socket.disconnect();
        console.log("stopping");
  });



});
