/*
    The main JS logic for Writing Center Scheduler
    Written by
    * Brandon Davis,
    * Moazzam Kahn,
    * Paul Kovach,
    * Ryan Court
    Fall 2016, COMP 523
*/

// GLOBAL VARIABLES
var me;
var loc;

/*
    This is the entry point for user_schedule.html
*/
var user_schedule_init = function(){
    // TODO...  implement
}

/*
    This is the entry point for location_settings.html
*/
var location_settings_init = function() {

    var table_div = $("#location-table");

    var select = $(".timeSelect");
    var hours, minutes, ampm;
    for(var i = 0; i <= 1440; i += 30){
        hours = Math.floor(i / 60);
        minutes = i % 60;
        if (minutes < 10){
            minutes = '0' + minutes; // adding leading zero
        }
        select.append($('<option></option>')
            .attr('value', i / 30)
            .text(hours + ':' + minutes));
    }

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
            try_expand_table(table_div, position);
        });
    }


    var path = location.pathname.split("/");
    var code = path[path.length -1];

    fetch_loc(code, function(obj){
        console.log(obj);
        loc=obj;

        if (obj != null){
            table_from_schedule(table_div, loc, loc.requirements, null, null, on_schedule_click);
        }
    });
}

/*
    This is the entry point for user_availability.html
    TODO: Click and drag range.
    TODO: Stretch goals.
*/
var user_availability_init = function(){

    var PID = $("#mypid").text();
    var table_div = $("#availability-table");

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
            try_expand_table(table_div, position);
        });
        // console.log(me);
    }

    fetch_me(PID, function(obj){
        console.log(obj);
        
        me=obj.user;

        if (obj != null){
            table_from_schedule(table_div, me, me.availability, obj.open, obj.close ,on_schedule_click);
        }

    });

}

/* --------------------------------

    Button-Triggered Functions

---------------------------------- */

var make_new_location = function(){
    var data = {};

    var Name = document.getElementById('name').value;
    // var Code = document.getElementById('code').value;
    //alert(Code);
    if (Name== ""  && Code=="") {
        alert("Fill Out All Feilds Before Submitting");
        return;
    }

    $("#new_loc").serializeArray().map(function(x){data[x.name] = x.value;});

    make_loc( data, function(obj){
        console.log(obj);
        sleep(100);
        location.reload();
    });
}

var meta_update_location = function(){
    var data = {};

    $("#existing_loc").serializeArray().map(function(x){data[x.name] = x.value;});

    loc.open_at = data.open_at;
    loc.close_at = data.close_at;
    loc.name = data.name
    loc.type_code = data.type_code;

    console.log(data);

    update_loc( loc.code, loc, function(obj){
        console.log(obj);
        sleep(100);
        location.reload();
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

var update_myself = function(){
    var data = {};
    $("#update_user").serializeArray().map(function(x){data[x.name] = x.value;});

    me.first_name = data['first_name'];
    me.last_name = data['last_name'];
    me.email = data['email'];
    me.desired_hours = data['desired_hours'];

    update_me(me, function(response){
        if (response['status'] == 'success'){
            $(".fa-check").show();
            $(".fa-check").text(" Success");
        } else {
            $(".fa-check").show();
            $(".fa-check").text(" Failed")
        }
    });
}

var update_schedule_nick = function(sid){
    var data = {};
    $("#schedule_nick").serializeArray().map(function(x){data[x.name] = x.value;});

    payload = {
        // it's important that this only have the "nick" field.  so that no other data is wiped out
        "nick": data['nick']
    }

    update_schedule(sid, payload, function(resp){
        console.log(resp);
    });
}

var csv_create_users = function(){
    var data = $("#csv-raw").val();
    bulk_create_users(data);
}

var confirm_delete_loc = function(code){
    if (confirm("Are you sure you want to delete " + code + "?") ){
        delete_loc(code, function(response){
            window.location = "/admin/location";
        });
    }
}

/*

Other Utilities

*/

var try_expand_table = function(table, position){
    var first = table.children("table:first").children("tr:first");
    var last = table.children("td:last");
    console.log(first);
}

var row_col_update = function(obj, table_div, cell){
    var rowcol = cell.id.substring(0, 3); // first three chars denotes the day
    var pos = cell.id.substring(3);

    if (rowcol == "row"){
        current = query_cell(obj, 'sun', pos);
    }
}

// Functions for opening new window upon click, supports mobile
$('a[target="_new"]').click(function() {
    return openWindow(this.href);
})

// Opens and resizes new window
// Unfortunately user settings may not allow opening new window, only new tab
function openWindow(url) {
    if (window.innerWidth <= 640) {
        // if width is smaller then 640px, create a temporary a elm that will open the link in new tab
        var a = document.createElement('a');
        a.setAttribute("href", url);
        a.setAttribute("target", "_blank");

        var dispatch = document.createEvent("HTMLEvents");
        dispatch.initEvent("click", true, true);

        a.dispatchEvent(dispatch);
    }
    else {
        var width = window.innerWidth * 0.66 ;
        // define the height in
        var height = width * window.innerHeight / window.innerWidth ;
        // Ratio the hight to the width as the user screen ratio
        window.open(url , 'newwindow', 'width=' + width + ', height=' + height + ', top=' + ((window.innerHeight - height) / 2) + ', left=' + ((window.innerWidth - width) / 2));
    }
    return false;
}
