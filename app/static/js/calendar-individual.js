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
    $(".footer").css("visibility", "hidden");
    $("#wrap").css("visibility", "hidden");
    var source = { url: window.location.href + '/data'};
    $.ajax({ //Fetch event information using ajax call to data page
        url : window.location.href + '/data',
        async:false,
        success : function(result){
            // console.log(result);
            $("#wrap").css("visibility", "visible");
            $(".footer").css("visibility", "visible");
            $(".loader").css("visibility", "hidden");
            source = result;
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
        eventLimit: true,
        events: source,
        // Mouseover event to see the pid of the scheduled employee,
        // Can be changed to display location name/code, employee name, etc.
        eventMouseover: function(event, jsEvent, view)
        {
            if (view.name !== 'agendaDay') {
                $(jsEvent.target).attr('title', String(event.pid) + '\n' + String(event._index) + '\n' + String(event.dow));
            }
        },
        // Renders events and filters based upon location
        eventRender: function eventRender(event, element, view )
        {
            return ['all', event.location].indexOf($('#location_selector').val()) >= 0;
        }
    });

    /* Initialize the location filter selector
    ------------------------------*/
    $('#location_selector').on('change',function(){
        $('#calendar').fullCalendar('rerenderEvents');
    });

});
