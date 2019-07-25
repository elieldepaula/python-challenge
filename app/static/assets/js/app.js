$(function(){

    // Loading.
    $body = $("body");
    $(document).on({
        ajaxStart: function() { $body.addClass("loading");    },
        ajaxStop: function() { $body.removeClass("loading"); }    
    });

    // List available containers on load.
    listContainers();

});

/**
 * List all containers into front-end.
 */
function listContainers()
{
    $.getJSON("/api/list").done(function(data){
        obj = data.containers;
        link = '';
        for (var i = 0; i < obj.length; i++) {
            if (obj[i].status == 'running') {
                link = '<buttom type="buttom" class="btn btn-danger" onclick="stopContainer(\''+obj[i].name+'\')"><i class="fa d-inline fa-stop"></i> Stop</buttom>';
            } else {
                link = '<buttom type="buttom"  href="#" class="btn btn-success" onclick="startContainer(\''+obj[i].name+'\')"><i class="fa d-inline fa-play"></i> Start</buttom>';
            }
            $('#tableRows').append('<tr><td>'+i+'</td><td>'+obj[i].name+'</td><td>'+obj[i].status+'</td><td>'+link+'</td></tr>');
        }
    });
}

/**
 * Create a new container.
 */
function createNewContainer()
{
    var image_name = $("#image_name").val();
    $("#image_name").val("");
    $.post('/api/new', {"image_name":image_name}, function(){
        $('#tableRows').html("");
        listContainers();
    }).fail(function(){
        alert('Error starting container ' + containerName);
    });
}

/**
 * Start a single container.
 * @param containerName 
 */
function startContainer(containerName)
{
    $.get('/api/'+containerName+'/start', function(){
        $('#tableRows').html("");
        listContainers();
    }).fail(function(){
        alert('Error starting container ' + containerName);
    });
}

/**
 * Stop a single container.
 * @param containerName 
 */
function stopContainer(containerName)
{
    $.get('/api/'+containerName+'/stop', function(){
        $('#tableRows').html("");
        listContainers();
    }).fail(function(){
        alert('Error stoping container ' + containerName);
    });
}

/**
 * Stop ALL running containers.
 */
function stopAllContainers()
{
    $.get('/api/stop/all', function(){
        $('#tableRows').html("");
        listContainers();
    }).fail(function(){
        alert('Error stoping containers ');
    });
}