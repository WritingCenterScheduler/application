$(document).ready(function(){

    /* Initialize external droppable external-events
    ------------------------------*/
    $('#external-events .fc-event').each(function() {
      // store data so the calendar knows to render an event upon drop
      $(this).data('event', {
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
        navLinks: true,
        editable: true,
        droppable: true,
        eventLimit: true,
        events: {
            url: window.location.href + '/data',
        },
        // Mouseover event to see the pid of the scheduled employee,
        // Can be changed to display location name/code, employee name, etc.
        eventMouseover: function(event, jsEvent, view) {
            if (view.name !== 'agendaDay') {
                $(jsEvent.target).attr('title', event.pid);
            }
        },
        // Deletes an event
        eventDestroy: function(event, element, view)
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
            if (r===true)
              {
                  $('#calendar').fullCalendar('removeEvents', calEvent._id);
              }
        }
    });
});
