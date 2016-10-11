/* 
AJAX fetches ME from the server, 
then calls callback(user)
*/
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