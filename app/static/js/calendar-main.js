/**
 * @author Ryan Court
 * @summary Javascript for rendering schedule using fullCalendar & jQueryUI
 * @see https://fullcalendar.io/
 *     For calendar rendering and action hooks
 * @see http://jqueryui.com/
 *     For droppable page elements
 * @since 1.0.1
 */

/*
GLOBAL VARIABLES
*/
var sched;
var lcode;

$(document).ready(function(){

    /* Initialize data source for calendar events
    ------------------------------*/
    console.dir(current_user)
    $(".footer").css("visibility", "hidden");
    $("#wrap").css("visibility", "hidden");
    var source = { url: window.location.href + '/data'};
    var allEvents;
    initExternalEvents();
    $.ajax({ //Fetch event information using ajax call to data page
        url : window.location.href + '/data',
        async:false,
        success : function(result){
            // console.log(result);
            $("#wrap").css("visibility", "visible");
            $(".footer").css("visibility", "visible");
            $(".loader").css("visibility", "hidden");
            source = result;
            allEvents = result;
        }
    });

    /* Helper functions for setting default location for external draggable events.
    ------------------------------*/
    function selector_default(v)
    {
        if (v == 'all'){
            return String(document.getElementById("location_selector").options[1].value);
        }
        return v;
    }
    function selector_default_code(v)
    {
        if (v == 'all'){
            v = String(document.getElementById("location_selector").options[1].value)
            return $("[id=\'" + v +"\']").attr('data-code');
        }
        return $("[id=\'" + v +"\']").attr('data-code');
    }

    /* Initialize droppable external-events
    ------------------------------*/
    function initExternalEvents(){
        $('#external-events .fc-event').each(function() {
          // store data so the calendar knows to render an event upon drop
          // alert(document.getElementById("location_selector").value)
          $(this).data('event', {
            location: selector_default(String(document.getElementById("location_selector").value)),
            lcode: selector_default_code(String(document.getElementById("location_selector").value)),
            title: $.trim($(this).text()), // use the element's text as the event title
            pid: $(this).attr('id'),
            backgroundColor: $(this).attr("data-color"),
            textColor : '#000000',
            duration: '00:30:00',
            stick: true // maintain when user navigates (see docs on the renderEvent method)
          });
          // make the event draggable using jQuery UI
          $(this).draggable({
            zIndex: 999,
            revert: true,      // will cause the event to go back to its
            revertDuration: 0  //  original position after the drag
          });
        });
    }

    /* Initialize the calendar
    ------------------------------*/
    $('#calendar').fullCalendar({
        header: {
            left: 'listWeek,agendaWeek,agendaDay'
        },
        // customize the button names,
        // otherwise they'd all just say "list"
        views: {
            listDay: { buttonText: 'List Day' },
            listWeek: { buttonText: 'List Week' }
        },
        defaultView: 'agendaWeek',
        businessHours: [ // specify an array instead
            {
                dow: [ 1, 2, 3, 4, 5 ], // Monday, Tuesday, Wednesday
                start: '08:00', // 8am
                end: '18:00' // 6pm
            }
        ],
        displayEventTime: false,
        navLinks: true,
        editable: true,
        droppable: true,
        eventLimit: true,
        events: source,
        // Mouseover event to see the pid of the scheduled employee,
        // Can be changed to display location name/code, employee name, etc.
        eventMouseover: function(calEvent, jsEvent, view)
        {
            if (view.name !== 'agendaDay') {
                $(jsEvent.target).attr('title', String(calEvent.pid) + '\n' + String(calEvent._index) + '\n' + String(calEvent.dow));
            }
        },
        // Deletes an event
        eventDestroy: function(calEvent, element, view)
        {
            // alert("removing stuff");
        },
        // Clicking an event prompts the user for event deletion
        eventClick: function(calEvent, jsEvent, view)
        {
            var start = new Date(calEvent.start);
            start.setHours(start.getHours() + 5);
            var end = new Date(calEvent.end);
            end.setHours(end.getHours() + 5);
            var r=confirm("Delete " + calEvent.title + " at " + calEvent.location + ", from " + start.toLocaleTimeString() + " to " + end.toLocaleTimeString() + "?");
            if (r===true){
                  $('#calendar').fullCalendar('removeEvents', calEvent._id);
              }
        },
        drop: function(date, jsEvent, ui, resourceId)
        {
            // console.log('An external event has been dropped.')
        },
        eventDrop: function(event, delta, revertFunc)
        {
            s = event.start.toDate();
            event._index = (((s.getHours() + 5) * 2) + (s.getMinutes() / 30));
            event.dow = event.start.day();
            e = event.end.toDate();
            event._endex = (((e.getHours() + 5) * 2) + (e.getMinutes() / 30));
        },
        eventReceive: function(event)
        {
            s = event.start.toDate();
            event._index = (((s.getHours() + 5) * 2) + (s.getMinutes() / 30));
            event.dow = event.start.day();
            e = event.end.toDate();
            event._endex = (((e.getHours() + 5) * 2) + (e.getMinutes() / 30));
        },
        eventResize: function(event, delta, revertFunc)
        {
            s = event.start.toDate();
            event._index = (((s.getHours() + 5) * 2) + (s.getMinutes() / 30));
            event.dow = event.start.day()
            e = event.end.toDate();
            event._endex = (((e.getHours() + 5) * 2) + (e.getMinutes() / 30));
        },
        // Renders events and filters based upon location
        eventRender: function eventRender(event, element, view )
        {
            return ['all', event.location].indexOf($('#location_selector option:selected').val()) >= 0 && ['all', event.pid].indexOf($('#pid_selector option:selected').val()) >= 0;
        }
    });

    $('#external-events .fc-event').on('click',function(){
        //alert($(this).val());
    });

    /* Initialize the location filter selector
    ------------------------------*/
    $('#location_selector').on('change',function(){
        initExternalEvents();
        $('#calendar').fullCalendar('rerenderEvents');
    });

    /* Initialize the pid filter selector
    ------------------------------*/
    $('#pid_selector').on('change',function(){
        $('#calendar').fullCalendar('rerenderEvents');
    });

    var json_sched;
    function ajaxCallBack(retVal){
        json_sched = retVal;
        console.log(retVal);
    }
    var lcode;
    function _ajaxCallBack(retVal){
        lcode = retVal;
    }
    $('#save-changes').on('click', function () {
        var conf = confirm("Save changes to schedule?\nWARNING: This will overwrite the existing schedule.");
        if (conf == false){return;}
        $("location_selector").prop('selectedIndex', 0);
        $.ajax({ //Fetch event information using ajax call to data page
            url : window.location.href + '/json',
            async:false,
            success : function(result){
                ajaxCallBack(result);
            }
        });
        // console.log(json_sched['data'][0]['schedule']['sun'][20]);
        var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
        for (var i = 0, len = days.length; i < len; i++){
            for (var j = 0, jlen = json_sched["data"].length; j < jlen; j++){
                for (var k = 0, klen = json_sched["data"][j]["schedule"][days[i]].length; k < klen; k++){
                    for(var l = 0, llen = json_sched["data"][j]["schedule"][days[i]][k].length; l < llen; l++){
                        if (json_sched["data"][j]["schedule"][days[i]][k][l] != null){
                            json_sched["data"][j]["schedule"][days[i]][k][l] = null;
                        }
                    }
                }
            }
        }
        // console.dir(json_sched['data'][0]['schedule']['sun'][20]);
        // console.log(json_sched['data'][0]['schedule']['sun'][20]);
        // console.dir(json_sched['data'][0]['schedule']['sun'][22]);
        var events = [];
        for(var i = 0, len = $('#calendar').fullCalendar('clientEvents').length; i < len; i++){
            events.push($('#calendar').fullCalendar('clientEvents')[i]);
        }
        //console.dir(events[1]._index)
        dows = {"0":"sun","1":"mon","2":"tue","3":"wed","4":"thu","5":"fri","6":"sat"};
        // console.dir(json_sched["data"][0]["schedule"][dows[String(events[1].dow)]][events[1]._index][0]);
        for (var i = 0, len = events.length; i < len; i++) {
            for (var j = 0, dlen = json_sched["data"].length; j < dlen; j++){
                if (String(events[i].lcode) == String(json_sched["data"][j]["code"])){
                    for (var l = 0, llen = events[i]._endex - events[i]._index; l < llen; l++){
                        for (var k = 0, klen = json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index].length; k < klen; k++){
                            if (json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index + l][k] == null){
                                json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index + l][k] = events[i].pid;
                                k = klen;
                            }
                        }
                    }
                }
            }
        }
        sched = {}
        sched.data = json_sched.data;
        sched.created_on = json_sched.created_on;
        var dateStr = new Date(json_sched['created_on']['$date']);
        var utcDate = dateStr.toUTCString();
        sched.created_on = utcDate
        update_schedule(json_sched['sid'], sched, function(response){
            if (response['status'] == 'success'){
                console.log('Successfully updated schedule!');
            } else {
                console.log('Unable to update schedule.')
            }
        });
    });

    $('#save-new').on('click', function () {
        var conf = confirm("Save changes as a new schedule?\nThis will create a new schedule accessible from the Admin page.");
        if (conf == false){return;}
        $("location_selector").prop('selectedIndex', 0);
        $.ajax({ //Fetch event information using ajax call to data page
            url : window.location.href + '/json',
            async:false,
            success : function(result){
                ajaxCallBack(result);
            }
        });
        // console.log(json_sched['data'][0]['schedule']['sun'][20]);
        var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
        for (var i = 0, len = days.length; i < len; i++){
            for (var j = 0, jlen = json_sched["data"].length; j < jlen; j++){
                for (var k = 0, klen = json_sched["data"][j]["schedule"][days[i]].length; k < klen; k++){
                    for(var l = 0, llen = json_sched["data"][j]["schedule"][days[i]][k].length; l < llen; l++){
                        if (json_sched["data"][j]["schedule"][days[i]][k][l] != null){
                            json_sched["data"][j]["schedule"][days[i]][k][l] = null;
                        }
                    }
                }
            }
        }

        var events = [];
        for(var i = 0, len = $('#calendar').fullCalendar('clientEvents').length; i < len; i++){
            events.push($('#calendar').fullCalendar('clientEvents')[i]);
        }
        //console.dir(events[1]._index)
        dows = {"0":"sun","1":"mon","2":"tue","3":"wed","4":"thu","5":"fri","6":"sat"};
        // console.dir(json_sched["data"][0]["schedule"][dows[String(events[1].dow)]][events[1]._index][0]);
        for (var i = 0, len = events.length; i < len; i++) {
            for (var j = 0, dlen = json_sched["data"].length; j < dlen; j++){
                if (String(events[i].lcode) == String(json_sched["data"][j]["code"])){
                    for (var l = 0, llen = events[i]._endex - events[i]._index; l < llen; l++){
                        for (var k = 0, klen = json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index].length; k < klen; k++){
                            if (json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index + l][k] == null){
                                json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i]._index + l][k] = events[i].pid;
                                k = klen;
                            }
                        }
                    }
                }
            }
        }
        sched = {};
        sched.data = json_sched.data;
        sched.created_on = json_sched.created_on;
        var dateStr = new Date(json_sched['created_on']['$date']);
        var utcDate = dateStr.toUTCString();
        sched.created_on = utcDate;
        //console.dir(sched)
        make_schedule(sched, function(response){
            if (response['status'] == 'success'){
                console.log('Successfully saved changes to new schedule!');
                //console.dir(response['lcode'])
                lcode = response['lcode']
                //_ajaxCallBack(response['lcode']);
                url = window.location.origin + "/api/schedule/" + String(lcode);
                openWindow(url);
                location.reload()
            } else {
                console.log('Unable to save changes to new schedule.');
            }
        });
    });
});
