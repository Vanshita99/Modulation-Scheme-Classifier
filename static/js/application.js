var socket;
function send_settings(data){
    $.get('http://' + document.domain + ':' + location.port + '/settings/'+data, function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  });
}


$(document).ready(function(){
    //connect to the socket server.
     
    var str1 = "data:image/png;base64,";

    //receive details from server
  $('#start').on('click',function(){
        socket=io.connect('http://' + document.domain + ':' + location.port + '/test');
        socket.connect();
        socket.on('newnumber', function(msg) {
            console.log("received");
            
            $.ajax({url: "get_image", success: function(result){
                $('#div_img').html("");
                $('#div_img').html('<img src="data:image/png;base64,' + result + '" />');
            }});
            
        });
  }); 

  $("#settings input[name='model_type']").click(function(){
    alert('You clicked radio!');
    if($('input:radio[name=model_type]:checked').val() == "cnn"){
        alert($('input:radio[name=type]:checked').val());
        //$('#select-table > .roomNumber').attr('enabled',false);
    }
});

  $('#cnn').on('click', function() {
    var settingObject = new Object();
    settingObject.cnn = true;
    settingObject.lstm = false;
    send_settings(JSON.stringify(settingObject));
  });

  $('#lstm').on('click', function() {
    var settingObject = new Object();
    settingObject.cnn = false;
    settingObject.lstm = true;
    send_settings(JSON.stringify(settingObject));
  });

  



  $('#stop').on('click',function(){
        socket.disconnect();
        console.log("stopping");
  });



});
