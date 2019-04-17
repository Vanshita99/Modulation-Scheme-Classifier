
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var str1 = "data:image/png;base64,";

    //receive details from server
  $('#btn').on('click',function(){
        socket.on('newnumber', function(msg) {
            console.log("received");
            
            $.ajax({url: "get_image", success: function(result){
                $('#div_img').html("");
                $('#div_img').html('<img src="data:image/png;base64,' + result + '" />');
            }});
            
        });
  }); 

});
