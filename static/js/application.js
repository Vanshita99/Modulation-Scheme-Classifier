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

  $('#cnn').on('click',function(){
        socket.cnn();
        console.log("cnn");
  });

  $('#lstm').on('click',function(){
        socket.()lstm
        console.log("lstm");
  });

  $('#stop').on('click',function(){
        socket.disconnect();
        console.log("stopping");
  });



});
