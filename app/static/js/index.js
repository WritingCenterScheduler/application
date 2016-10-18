/*
    The main JS logic for Writing Center Scheduler
    Written by BD, MK, PK, and RC
    Fall 2016, COMP 523
*/

var user_availability_init = function(){
    /*
        This is the entry point for user_availability.html
        TODO: color for availability.
        TODO: Click and drag range.
        TODO: Stretch goals.
    */
    var me;

    var on_schedule_click = function(cell){
        day = cell.id.substring(0, 3);
        position = cell.id.substring(3);
        var current = me['availability'][day][position];
        
        if (current == 0){
            cell.innerText = 1;
            me['availability'][day][position] = 1;
        }
        else if (current == 1){
            cell.innerText = 2;
            me['availability'][day][position] = 2;
        }
        else if (current == 2){
            cell.innerText = 0;
            me['availability'][day][position] = 0;
        }
        // TODO: Update the backend.
        update_me(me, function(response){
            console.log(response);
        });
        // console.log(me);
    }

    fetch_me(function(obj){
        console.log("ASDF");
        console.log(obj);
        me=obj;
        
        if (obj != null){
            table_doc = $("#inputTable");
            table_from_schedule(table_doc, obj, on_schedule_click);
        }
    });
}