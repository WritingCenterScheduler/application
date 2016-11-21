$(document).ready(function(){
    alert(window.location.href + '/data')
    $('#calendar').fullCalendar({
        header: {
            right: 'month,agendaWeek,agendaDay'
        },
        events: {
                url: window.location.href + '/data',
        },
        defaultView: 'agendaWeek',
        loading: function(bool) {
                $('#loading').toggle(bool);
        }
    });
});
