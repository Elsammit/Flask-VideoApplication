let count = 0;
$( function() {
    $('#Start').on('click',
    function() {
        var slides = $(".InputTab > div");
        count = (count+1) % 2;
        console.log("count:"+count);
        slides.removeClass("current").eq(count).addClass("current");
        console.log("start Clcik");
        if(count == 1){
            var hostUrl= '/start';
        }else{
            var hostUrl= '/pause';
        }
        
        $.ajax({
            url: hostUrl,
            type:'POST',
            timeout:3000,
        }).done(function() {
            console.log("ok");
        }).fail(function() {
            console.log("error");
        })
    });
} );

$( function() {
    $('#Stop').on('click',
    function() {
        console.log("stop Clcik");
        count = 1;
        var slides = $(".InputTab > div");
        slides.removeClass("current").eq(count).addClass("current");
        var hostUrl= '/stop';
        $.ajax({
            url: hostUrl,
            type:'POST',
            timeout:3000,
        }).done(function() {
            console.log("ok");
        }).fail(function() {
            console.log("error");
        })
    });
} );

$( function() {
    $('#Rewind').on('click',
    function() {
        console.log("start Clcik");
        var hostUrl= '/rewind';
        $.ajax({
            url: hostUrl,
            type:'POST',
            timeout:3000,
        }).done(function() {
            console.log("ok");
        }).fail(function() {
            console.log("error");
        })
    });
} );

$( function() {
    $('#Speed').on('click',
    function() {
        console.log("speed Clcik");
        var hostUrl= '/speed';
        $.ajax({
            url: hostUrl,
            type:'POST',
            timeout:3000,
        }).done(function() {
            console.log("ok");
        }).fail(function() {
            console.log("error");
        })
    });
} );


setInterval(function(){
    var hostUrl= '/progress';

    $.ajax({
        url: hostUrl,
        type:'POST',
        timeout:3000,
    }).done(function(data) {
        console.log(data);
        seekClass = document.getElementById("sekbar");
        seekClass.style.width = String(data)+'%'; 
    }).fail(function() {
        console.log("error");
    })
}, 1000);

function changeImages(obj){
    console.log("call changeImages");
    var fileReader = new FileReader();  // フォルダを開き画像選択させる.
    fileReader.onload = (function(){
        document.getElementById("upfile").src = fileReader.result;  
        console.log("file upload : " + fileReader.result);
    });
    console.log(document.getElementById("upfile").files[0]);
    console.log(document.getElementById("upfile").files[0].size);
    var formdata = new FormData($('#my_form').get(0));
    console.log(formdata);
    var hostUrl= '/test';
        $.ajax({
            url: hostUrl,
            type:'POST',
            data:document.getElementById("upfile").files[0].size,
            timeout:3000,
        }).done(function() {
            console.log("ok");
        }).fail(function() {
            console.log("error");
        })
}