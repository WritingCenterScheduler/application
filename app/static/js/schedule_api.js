/*
    Written by 
    * Brandon Davis, 
    * Moazzam Kahn,
    * Paul Kovach,
    * Ryan Court
    
    Fall 2016, COMP 523
*/

var MINUTESPERDAY = 60 * 24;
var TFS_CLICK_CALLBACK_FN;
var BEGIN_TABLE=16;//16;
var END_TABLE=34;//34;

/*
    UTILS
*/

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

String.prototype.replaceAt=function(index, character) {
    return this.substr(0, index) + character + this.substr(index+character.length);
}

function make_schedule_payload(sched_string, payload_json){
    var rtrn = {};
    rtrn[sched_string] = payload_json.availability;
    return rtrn;
}

/*
    ME
*/

function fetch_me(pid, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", "/api/user/"+pid, true);
    xhttp.send();
}


function update_me(user_object, callback){
    if (user_object.pid == null){
        alert("User loaded improperly.");
    }

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };

    xhttp.open("PUT", "/api/user/" + user_object.pid, true);
    xhttp.send(JSON.stringify(user_object));
}

/*
    LOCATION
*/

function fetch_loc(code, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", "/api/location/" + code, true);
    xhttp.send();
}


function update_loc(code, payload_json, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("PUT", "/api/location/" + code, true);
    xhttp.send(JSON.stringify(payload_json));
}


function make_loc(payload_json, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("POST", "/api/locations", true);
    xhttp.send(JSON.stringify(payload_json));
}


function delete_loc(code, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("DELETE", "/api/location/" + code, true);
    xhttp.send();
}

/*
    USER ADMIN
*/

function make_user(payload_json, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("POST", "/api/user", true);
    xhttp.send(JSON.stringify(payload_json));
}


function delete_user(pid){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    if (confirm("Delete user " + pid + " ?\nThis cannot be undone.")){
        xhttp.open("DELETE", "/api/user/" + pid, true);
        xhttp.send();
    }
}

function toggle_bit(PID, bit, typecode){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    xhttp.open("PUT", "/api/user/" + PID , true);

    var newcode = typecode.charAt(bit) == '1' ? '0' : '1';
    typecode = typecode.replaceAt(bit, newcode);

    xhttp.send(JSON.stringify({
        "typecode": typecode
    }));
}

function bulk_create_users(payload){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    xhttp.open("POST", "/api/user/bulkcreate", true);
    xhttp.send(payload);
}

function randomize_user_color(PID){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    if (confirm("Generate new color for this user?\nThis cannot be undone.")){
        xhttp.open("POST", "/api/user/" + PID + "/colorize", true);
        xhttp.send();
    }
}

/*
    SCHEDULE
*/

function toggle_active(SID){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    xhttp.open("GET", "/api/schedule/" + SID + "/activate", true);
    xhttp.send();
}

function run_schedule(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            // callback(JSON.parse(this.responseText));
            // cause a reload
            location.reload();
            $(".fa.fa-refresh").hide();
        }
    };
    xhttp.open("GET", "/admin/runschedule", true);
    xhttp.send();

    // hide the spinner when we're done.
    $(".fa.fa-refresh").show();
}


function delete_schedule(code){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            location.reload();
        }
    };
    if (confirm("Delete schedule? " + code)){
        xhttp.open("DELETE", "/api/schedule/" + code, true);
        xhttp.send();
    }
}

function update_schedule(code, payload_json, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("PUT", "/api/schedule/" + code, true);
    xhttp.send(JSON.stringify(payload_json));
}


function table_from_schedule(table_div, schedule_meta, schedule_data, click_callback){
    TFS_CLICK_CALLBACK_FN = click_callback;
    var slots = MINUTESPERDAY / schedule_meta.resolution_minutes;
    var newtable = $("<table id='user-schedule'>\
        <tr>\
            <th> Time </th>\
            <th id='colsun' onclick='tfs_click_callback(this)' > Sunday </th>\
            <th id='colmon' onclick='tfs_click_callback(this)'> Monday </th>\
            <th id='coltue' onclick='tfs_click_callback(this)'> Tuesday </th>\
            <th id='colwed' onclick='tfs_click_callback(this)'> Wednesday </th>\
            <th id='colthu' onclick='tfs_click_callback(this)'> Thursday </th>\
            <th id='colfri' onclick='tfs_click_callback(this)'> Friday </th>\
            <th id='colsat' onclick='tfs_click_callback(this)'> Saturday </th>\
        </tr>\
        </table>");
    table_div.append(newtable);
    var resolution = schedule_meta.resolution_minutes / 60;

    var first_event_index = slots-1;
    var last_event_index = 0;
    var day_keys = Object.keys(schedule_data);

    // Determine where the events begin...
    // for(var i = 0; i < slots; i++){
    //     for (var k = 0; k < day_keys.length; k++){
    //         if (schedule_data[day_keys[k]][i] != 0 && i < first_event_index){
    //             first_event_index = i;
    //         }
    //         if (schedule_data[day_keys[k]][i] != 0 && i > last_event_index){
    //             last_event_index = i;
    //         }
    //     }
    // }

    if (schedule_meta.open_at != null){
        first_event_index = parseInt(schedule_meta.open_at);
        last_event_index = parseInt(schedule_meta.close_at);
    } else {
        first_event_index=BEGIN_TABLE;
        last_event_index=END_TABLE;
    }


    for(var i = 0; i < slots; i++){

        if (i < first_event_index || i > last_event_index ){
            // do nothing
            continue;
        }
        var hour = Math.floor(i*resolution);
        var minute_decimal = (i*resolution) - hour;
        var min = Math.floor(minute_decimal*60);
        if(min==0) {
            min = "00"
        }
        var newrow = $("<tr> \
           <td id='col"+i+"' class='time' onclick='tfs_click_callback(this)'> " + hour + ":"+ min+"</td>\
           <td class = table-"+schedule_data["sun"][i]+" id='sun"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["sun"][i]+"</td> \
           <td class = table-"+schedule_data["mon"][i]+" id='mon"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["mon"][i]+"</td> \
           <td class = table-"+schedule_data["tue"][i]+" id='tue"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["tue"][i]+"</td> \
           <td class = table-"+schedule_data["wed"][i]+" id='wed"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["wed"][i]+"</td> \
           <td class = table-"+schedule_data["thu"][i]+" id='thu"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["thu"][i]+"</td> \
           <td class = table-"+schedule_data["fri"][i]+" id='fri"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["fri"][i]+"</td> \
           <td class = table-"+schedule_data["sat"][i]+" id='sat"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_data["sat"][i]+"</td> \
        </tr>");
        newtable.append(newrow);
    }
}


var tfs_click_callback = function(event){
    TFS_CLICK_CALLBACK_FN(event);
}
