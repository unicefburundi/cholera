'use strict';

$(document).ready(function(){
    $('#selectbox1').on("change", function(){
    $.get("/get_districts/"+$('#selectbox1').val(),
            function (data){
              $('#selectbox2').html(data);
            }
        , "html")
        });
    $('#selectbox2').on("change", function(){
    $.get("/get_cdss/"+$('#selectbox2').val(),
            function (data){
              $('#selectbox3').html(data);
            }
        , "html")
        });

});