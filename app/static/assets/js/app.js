$(document).ready(function () {

    /* $.get("/api/list").done(function (data) {
        for(row in data){
            console.log(row.containers.id);
        }
        // console.log(data);
    }).fail(function(){
        alert("Errouu!")
    });*/

    listContainers();


});

/**
 * List all containers into front-end.
 */
function listContainers()
{
    $.getJSON("/api/list").done(function(data){
        $.each(data function(i, item){
            $('td') .html(
                $('td').text(item.id),
                $('td').text(item.name)
            ).appendTo("#tableRows");
        })
    });
}
