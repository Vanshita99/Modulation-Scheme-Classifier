var socket;
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

  $('#stop').on('click',function(){
        socket.disconnect();
        console.log("stopping");
  });

});
