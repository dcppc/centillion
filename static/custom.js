var result = "";

function load_gdocs_table(){

    $.getJSON("/list/gdoc", function(result){
        $.each(result, function(k, field){
            //$("div").append(field + " ");
            console.log('---');
            console.log(k);
            console.log(field);
        });
    });
    console.log('hello world');
}

