$(document).ready(function(){
    $('select[name=province]').change(function(){
            province_id = $(this).val();
            request_url = '/get_districts/' + province_id + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    $('select[name=districts]').val(''); // remove the value from the input
                    console.log(data); // log the returned json to the console
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
                    $('select[id=id_cds]').val(''); // remove the value from the input
                    console.log(data); // log the returned json to the console
                    $.each(data[0], function(key, value){
                        $('select[id=id_cds]').append('<option value="' + key + '">' + value +'</option>');
                    })
                }
            })
        });
     $('select[name=profile-level]').click(function() {
            level = $(this).val();
            console.log(level);
            if (level == ''){
                level = 'CEN'
            }
            request_url = '/get_by_level/' + level + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    console.log(data);
                    $('select[name=facility]').empty(); // remove the value from the input
                    $.each(data[0], function(key, value){
                        $('select[name=facility]').append('<option value="' + key + '">' + value +'</option>');
                    })
                }
            });
            return false; //<---- move it here
        });
     $('select[name=facility]').click(function() {
            facility = $(this).val();
            document.getElementById('id_profile-moh_facility').value = parseInt(facility);
        });
    });