$('form').submit(function(){
    $('#waiting').show();
    $(this).children('input[type=submit]').prop('disabled', true);
   });