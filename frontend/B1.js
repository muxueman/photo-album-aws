$(document).ready(function(){
    var apigClient = apigClientFactory.newClient();
    var apigClient = apigClientFactory.newClient({
        apiKey: ''
    });
    
    $("#search").click(function(){
        var q = $('#query').val();
        console.log("q: ", q)
        var params = {  
            'q': q 
        }
        var additionalParams = {}
        var body = {}

        apigClient.searchGet(params, body, additionalParams).then(function(result){
            console.log("success");
            var data = result.data; 
            console.log(data);

            // create div for image display
            if ($(".photo").length === 0){
                $(".container").append('<br><div class="photo" ></div>');
                if (data.length == 0){
                    $(".photo").append('<label>No result!</label><br>');
                }else{
                    $(".photo").append('<label>Search Result:</label><br>');
                }
            }else{
                $(".photo").empty();
                $(".photo").append('<label>Search Result:</label><br>');
            }

            // display image
            for (i = 0; i < data.length; i++){
                var url = data[i];
                $(".photo").append('<img src="' + url + '" >');
            }
        }).catch(function(result){
            console.log("error");
            console.log(result);
            var data = result.data; 
            console.log(data);
        });
    });

    function getBase64(file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => {
            let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
            if ((encoded.length % 4) > 0) {
              encoded += '='.repeat(4 - (encoded.length % 4));
            }
            resolve(encoded);
          };
          reader.onerror = error => reject(error);
        });
    }
    
    $("#upload").click(function(){
        var f = $('#file').prop('files')[0];
        if(f){
            if (!f.type.match('image.*')) {
                alert("File must be image.");
                return false;
            }

            var encoded_image = getBase64(f).then(
                data => {
                console.log(data);
                var body = {data};
                var params = {
                    "item" : f.name, 
                    "folder" : "photo-album-hw3", 
                    "Content-Type" : f.type + ";base64"
                    
                };
                
                var additionalParams = {};
                apigClient.folderItemPut(params, body, additionalParams).then(function(result){
                    console.log("success.");
                    console.log(result);
                    var data = result.data; 
                    console.log(data);
                }).catch(function(result){
                    console.log("failed.");
                    console.log(result);
                    var data = result.data; 
                    console.log(data);
                });

            });
        }
    });
    
});