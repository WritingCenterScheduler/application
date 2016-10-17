/* 
AJAX fetches ME from the server, 
then calls callback(user)
*/

var MINUTESPERDAY = 60 * 24;

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
    xhttp.send(JSON.stringify(user_object));   
}

function table_from_schedule(table_div, schedule_object){
    var karr = Object.keys(schedule_object);
    var slots = MINUTESPERDAY / schedule_object.resolution_minutes;
    var newtable = $("<table id='user-schedule'>\
        <tr>\
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
    for(var i = 0; i < slots; i++){
        var newrow = $("<tr> \
           <td>"+schedule_object.availability["sun"][i]+"</td> \
           <td>"+schedule_object.availability["mon"][i]+"</td> \
           <td>"+schedule_object.availability["tue"][i]+"</td> \
           <td>"+schedule_object.availability["wed"][i]+"</td> \
           <td>"+schedule_object.availability["thu"][i]+"</td> \
           <td>"+schedule_object.availability["fri"][i]+"</td> \
           <td>"+schedule_object.availability["sat"][i]+"</td> \
        </tr>");
        newtable.append(newrow);
    }
}