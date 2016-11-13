/*
    The main JS logic for Writing Center Scheduler
    Written by BD, MK, PK, and RC
    Fall 2016, COMP 523
*/

var location_settings_init = function() {
    /*
        This is the entry point for location_settings.html
    */
    var loc;

    var on_schedule_click = function(cell){
        day = cell.id.substring(0, 3); // first three chars denotes the day
        position = cell.id.substring(3); // the rest of the string denotes position
        var current = loc["requirements"][day][position];
        
        if (current == 0){
            cell.innerText = 1;
            cell.className = 'table-1';
            loc["requirements"][day][position] = 1;
        }
        else if (current == 1){
            cell.innerText = 2;
            cell.className = 'table-2';
            loc["requirements"][day][position] = 2;
        }
        else if (current == 2){
            cell.innerText = 0;
            cell.className= 'table-0';
            loc["requirements"][day][position] = 0;
        }
        // TODO: Update the backend.
        update_loc(loc.code, loc, function(response){
            console.log(response);
        });
    }


    var path = location.pathname.split("/");
    var code = path[path.length -1];
    fetch_loc(code, function(obj){
        console.log(obj);
        loc=obj;
        
        if (obj != null){
            table_div = $("#location-table");
            table_from_schedule(table_div, loc, loc.requirements, on_schedule_click);

                var select = $(".timeSelect");
                var hours, minutes, ampm;
                for(var i = 0; i <= 1440; i += 30){
                    hours = Math.floor(i / 60);
                    minutes = i % 60;
                    if (minutes < 10){
                        minutes = '0' + minutes; // adding leading zero
                    }
                    select.append($('<option></option>')
                        .attr('value', i)
                        .text(hours + ':' + minutes));
                }

        }

    });




}

var make_new_location = function(){
    var data = {};

    var Name   = document.getElementById('name').value;
    var Code = document.getElementById('code').value;
    //alert(Code);
    if (Name== ""  && Code=="") {
        alert("Fill Out All Feilds Before Submitting");
        return;
    }

    $("#new_loc").serializeArray().map(function(x){data[x.name] = x.value;});

    make_loc( data, function(obj){
        console.log(obj);
    });


}

var make_new_user = function(){
    var data = {};
    $("#new_user").serializeArray().map(function(x){data[x.name] = x.value;});

    make_user(data, function(obj){
        console.log(obj);
        location.reload();
    });
}

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
            cell.className = 'table-1';
            me['availability'][day][position] = 1;
        }
        else if (current == 1){
            cell.innerText = 2;
            cell.className = 'table-2';
            me['availability'][day][position] = 2;
        }
        else if (current == 2){
            cell.innerText = 0;
            cell.className= 'table-0';
            me['availability'][day][position] = 0;
        }
        // TODO: Update the backend.
        update_me(me, function(response){
            console.log(response);
        });
        // console.log(me);
    }

    fetch_me(function(obj){
        console.log(obj);
        me=obj;
        
        if (obj != null){
            table_div = $("#availability-table");
            table_from_schedule(table_div, obj, obj.availability, on_schedule_click);
        }

    });

}
