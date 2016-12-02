/**
 * @author Ryan Court
 * @summary Javascript for rendering schedule using fullCalendar & jQueryUI
 * @see https://fullcalendar.io/
 *     For calendar rendering and action hooks
 * @see http://jqueryui.com/
 *     For droppable page elements
 * @since 1.0.1
 */
$(document).ready(function(){

    /* Initialize data source for calendar events
    ------------------------------*/
    var source = { url: window.location.href + '/data'};
    var allEvents;
    initExternalEvents();
    $.ajax({ //Fetch event information using ajax call to data page
        url : window.location.href + '/data',
        success : function(result){
            // console.log(result);
            source = result;
            allEvents = result;
        }
    });

    /* Helper function for setting default location for external draggable events.
    ------------------------------*/
    function selector_default(v)
    {
        if (v == 'all'){
            return String(document.getElementById("location_selector").options[1].value);
        }
        return v;
    }

    /* Initialize droppable external-events
    ------------------------------*/
    function initExternalEvents(){
        $('#external-events .fc-event').each(function() {
          // store data so the calendar knows to render an event upon drop
          // alert(document.getElementById("location_selector").value)
          $(this).data('event', {
            location: selector_default(String(document.getElementById("location_selector").value)),
            title: $.trim($(this).text()), // use the element's text as the event title
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
                $(jsEvent.target).attr('title', calEvent.pid);
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
        drop: function(date, calEvent, ui, resourceId)
        {
            alert("external drop: " + allEvents.length);
            $('#calendar').fullCalendar('addEvents', calEvent._id);
        },
        eventDrop: function(calEvent, delta, revertFunc)
        {
            alert("event drop: " + allEvents.length);
            $('#calendar').fullCalendar('addEvents', calEvent._id);
        },
        // Renders events and filters based upon location
        eventRender: function eventRender(calEvent, element, view )
        {
            //console.log(['all', calEvent.location][($('#location_selector').val()) >= 0 ? 1 : 0])
            return ['all', calEvent.location].indexOf($('#location_selector').val()) >= 0
        }
    });

    /* Initialize the location filter selector
    ------------------------------*/
    $('#location_selector').on('change',function(){
        filterEvents($('#location_selector').val());
        initExternalEvents();
        alert($('#calendar').fullCalendar('clientEvents').length);
        $('#calendar').fullCalendar('rerenderEvents');
    });

    $('#external-events .fc-event').on('click',function(){
        alert($(this).val());
    });

    function filterEvents(filter){
        var newSource = [];
        var events = [];
        for(var i = 0, len = $('#calendar').fullCalendar('clientEvents').length; i < len; i++){
            events.push($('#calendar').fullCalendar('clientEvents')[i]);
        }
        //alert(events)
        for (var i = 0, len = events.length; i < len; i++) {
            if (String(events[i].location) == String(filter))
            {
                newSource.push(events[i]);
            }
        }
        $('#calendar').fullCalendar('refetchEventSources', newSource);
    }

    var json_sched;
    function ajaxCallBack(retVal){
        json_sched = retVal;
    }

    $('#getJson').on('click', function () {
        $("location_selector").prop('selectedIndex', 0);
        $.ajax({ //Fetch event information using ajax call to data page
            url : window.location.href + '/json',
            async:false,
            success : function(result){
                ajaxCallBack(result);
            }
        });
        var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
        for (var i = 0, len = days.length; i < len; i++){
            for (var j = 0, jlen = json_sched["data"].length; j < jlen; j++){
                for (var k = 0, klen = json_sched["data"][j]["schedule"][days[i]].length; k < klen; k++){
                    for(var l = 0, llen = json_sched["data"][j]["schedule"][days[i]][k]; l < llen; l++){
                        json_sched["data"][j]["schedule"][days[i]][k][l] = null;
                    }
                }
            }
        }
        console.log(json_sched);
        var events = [];
        for(var i = 0, len = $('#calendar').fullCalendar('clientEvents').length; i < len; i++){
            events.push($('#calendar').fullCalendar('clientEvents')[i]);
        }
        dows = {"0":"sun","1":"mon","2":"tue","3":"wed","4":"thu","5":"fri","6":"sat"};
        for (var i = 0, len = events.length; i < len; i++) {
            for (var j = 0, dlen = json_sched["data"].length; j < dlen; j++){
                if (String(events[i].lcode) == String(json_sched["data"][j]["code"])){
                    json_sched["data"][j]["schedule"][dows[String(events[i].dow)]][events[i].index] = events[i].pid;
                }
            }
        }
        console.log(json_sched);
    });
});
