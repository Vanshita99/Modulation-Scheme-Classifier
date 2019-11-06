var socket;

var settings = new Object();

function send_settings() {
    data = JSON.stringify(settings);
    console.log("Sending settings with data = " + data);
    $.get('http://' + document.domain + ':' + location.port + '/settings/'+data, function(data, status){
  });

    console.log("v3 socket is ",socket);
}


function initSettings() {
  settings.cnn = false;
  settings.lstm = true;
  settings.band = 'two';
  settings.channel='AWGN';
  settings.snr='25';
  send_settings();
}

function set_model_cnn() {
  
        settings.cnn = true;
        settings.lstm = false;
        send_settings();
}

function set_model_lstm() {
 
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
        //initSettings();
        $("#start").prop('disabled', true);
        $("#stop").prop('disabled', false);
        socket=io.connect('http://' + document.domain + ':' + location.port + '/test');
        socket.connect();
        socket.on('newnumber', function(msg1,msg2) {
            console.log("received");
            
            $.ajax({url: "get_image", success: function(result){
                $('#div_img').html("");
                $('#div_img').html('<img class="img-responsive" style="width:100%;" src="data:image/png;base64,' + result + '" />');
            }});
            console.log(msg2)
            // $('#progressbar').progressbar({
            //     value : msg2
            // });
            $.getElementById('smname').value = msg2;

        });
        // socket.on('newnumber1', function(msg) {
        //     console.log("received");
        //     $('#log').html(msg.accuracy)
        //     });
            
        // });
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

  $('#channel_selector').on('change',function() {
    selectedChannel = $("#channel_selector").val();
    console.log(selectedChannel);
    if(selectedChannel != -1) {
      // do something something
      settings.channel = selectedChannel;
      send_settings();
    }
  });

  $('#SNR_selector').on('change',function() {
    selectedSNR = $("#SNR_selector").val();
    console.log(selectedSNR);
    if(selectedSNR != -1) {
      // do something something
      settings.snr = selectedSNR;
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
