/*
    The main JS logic for Writing Center Scheduler
    Written by BD, MK, PK, and RC
    Fall 2016, COMP 523
*/

var user_availability_init = function(){
    /*
        This is the entry point for user_availability.html
    */
    fetch_me(function(obj){
        console.log(obj);
        if (obj != null){
            table_div = $("#availability-table");
            table_from_schedule(table_div, obj);
        }
    });
}