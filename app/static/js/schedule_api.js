/* 
AJAX fetches ME from the server, 
then calls callback(user)
*/

var MINUTESPERDAY = 60 * 24;
var TFS_CLICK_CALLBACK_FN;
var BEGIN_TABLE=16;
var END_TABLE=34;

function make_availability_payload(payload_json){
    return {
        "availability": payload_json.availability
    }
}

function fetch_me(callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", "/api/user/me", true);
    xhttp.send();
}

function update_me(payload_json, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("PUT", "/api/user/me", true);
    xhttp.send(JSON.stringify(payload_json)); 
}

/*
AJAX updates ME on the server
then calls callback with the status
*/
function update_me(user_object, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xhttp.open("PUT", "/api/user/me", true);
    xhttp.send(JSON.stringify(make_availability_payload(user_object) ));   
}

function table_from_schedule(table_div, schedule_object, click_callback){
    TFS_CLICK_CALLBACK_FN = click_callback;
    var karr = Object.keys(schedule_object);
    var slots = MINUTESPERDAY / schedule_object.resolution_minutes;
    var newtable = $("<table id='user-schedule'>\
        <tr>\
            <th> Time </th>\
            <th> Sunday </th>\
            <th> Monday </th>\
            <th> Tuesday </th>\
            <th> Wednesday </th>\
            <th> Thursday </th>\
            <th> Friday </th>\
            <th> Saturday </th>\
        </tr>\
        </table>");
    table_div.append(newtable);
    var resolution = schedule_object.resolution_minutes / 60;
    for(var i = 0; i < slots; i++){

        if (i < BEGIN_TABLE || i > END_TABLE){
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
           <td id='time'> " + hour + ":"+ min+"</td>\
           <td class = table-"+schedule_object.availability["sun"][i]+" id='sun"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["sun"][i]+"</td> \
           <td class = table-"+schedule_object.availability["mon"][i]+" id='mon"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["mon"][i]+"</td> \
           <td class = table-"+schedule_object.availability["tue"][i]+" id='tue"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["tue"][i]+"</td> \
           <td class = table-"+schedule_object.availability["wed"][i]+" id='wed"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["wed"][i]+"</td> \
           <td class = table-"+schedule_object.availability["thu"][i]+" id='thu"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["thu"][i]+"</td> \
           <td class = table-"+schedule_object.availability["fri"][i]+" id='fri"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["fri"][i]+"</td> \
           <td class = table-"+schedule_object.availability["sat"][i]+" id='sat"+i+"' onclick='tfs_click_callback(this)'>"+
            schedule_object.availability["sat"][i]+"</td> \
        </tr>");
        newtable.append(newrow);
    }
}

var tfs_click_callback = function(event){
    TFS_CLICK_CALLBACK_FN(event);
}
