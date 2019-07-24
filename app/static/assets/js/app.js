$(document).ready(function () {

    $.get("/api/list").done(function (data) {
        for(row in data){
            console.log(row.containers.id);
        }
        // console.log(data);
    }).fail(function(){
        alert("Errouu!")
    });

});