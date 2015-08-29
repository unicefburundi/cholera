$(document).ready(function(){
    $('select[name=province]').change(function(){
            province_id = $(this).val();
            request_url = '/get_districts/' + province_id + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    $.each(data[0], function(key, value){
                        $('select[name=districts]').append('<option value="' + key + '">' + value +'</option>');
                    })
                }
            });
            return false; //<---- move it here
        });
    $('select[name=districts]').change(function(){
            district_id = $(this).val();
            request_url = '/get_cdss/' + district_id + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    $.each(data[0], function(key, value){
                        $('select[id=id_cds]').append('<option value="' + key + '">' + value +'</option>');
                    })
                }
            })
        })
    });