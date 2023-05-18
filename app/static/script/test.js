// {% extends "base.html" %}
// {% block mycontent %}

// <head>
//     <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
//     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.7/index.global.min.css">
//     <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.7/index.global.min.js"> </script>
//     <title>{{user.username}}'s Home</title>
// </head>

// <body>
//     <center>
//         <picture>
//             <img src="https://media.discordapp.net/attachments/758931822368784434/1086463776959762472/Screenshot_2023-03-17_at_6.39.05_PM.png?width=1007&height=297" alt="pladdict logo" style="width:340px;height:100px;">
//         </picture>

//         {% for message in get_flashed_messages() %}
//             <div class="alert alert-warning alert-dismissible fade show" role="alert">
//                 {{ message }}
//                 <button type="button" class="close" data-dismiss="alert" aria-label="Close">
//                 <span aria-hidden="true">&times;</span>
//                 </button>
//             </div>
//         {% endfor %}

//         <div class = "greeting">
//             Welcome to pladdict! <br>
//             Hello {{user.username}}
//         </div>
//         <br>
//         <br>
//         <div id='calendar'></div>
//         <script>
//           document.addEventListener('DOMContentLoaded', function() {
//             var calendarEl = document.getElementById('calendar');
        
//             var calendar = new FullCalendar.Calendar(calendarEl, {

//               events : [
//                   {% for event in events %}
//                     {
//                         title : '{{event.plant}}',
//                         startTime : '{{event.startDate}}T00:00:00',
//                         end: '14:00',
//                         {% if event.recurring == 'Frequent'%}
//                             daysOfWeek: [1,4],
//                         {% elif event.recurring == 'Average' %}
//                             daysOfWeek: [3],    
//                         {% else %}
                        
//                         {% endif %}
//                     },
//                   {% endfor %}
//               ]

//             // events: [
//             // {
//             //     // groupId: 'blueEvents', // recurrent events in this group move together
//             //     daysOfWeek: [ '4' ],
//             //     // startTime: '10:45:00',
//             //     // endTime: '12:45:00'
//             // },
//             // ]
//             });
        
//             calendar.render();
//           });
//         </script>
//     </center>
        
// </body>

// <!-- {% for plant in plant_data %}
//     {{ plant.common_name }} {{ plant.watering }} {{ (plant.start_date.strftime('%Y-%m-%d')) }}
//     <br />
// {% endfor %} -->
// {{plant_data}}

// {% endblock %}

// <!-- <script>
// var defaultEvents = [
// {
// // Just an event
// title: 'Long Event',
// start: '2017-02-07',
// end: '2017-02-10',
// className: 'scheduler_basic_event'
// },
// {
// // Custom repeating event
// id: 999,
// title: 'Repeating Event',
// start: '2017-02-09T16:00:00',
// className: 'scheduler_basic_event'
// },
// {
// // Custom repeating event
// id: 999,
// title: 'Repeating Event',
// start: '2017-02-16T16:00:00',
// className: 'scheduler_basic_event'
// },
// {
// // Just an event
// title: 'Lunch',
// start: '2017-02-12T12:00:00',
// className: 'scheduler_basic_event',
// },
// {
// // Just an event
// title: 'Happy Hour',
// start: '2017-02-12T17:30:00',
// className: 'scheduler_basic_event'
// },
// {   
// // Monthly event
// id: 111,
// title: 'Meeting',
// start: '2000-01-01T00:00:00',
// className: 'scheduler_basic_event',
// repeat: 1
// },
// {
// // Annual avent
// id: 222,
// title: 'Birthday Party',
// start: '2017-02-04T07:00:00',
// description: 'This is a cool event',
// className: 'scheduler_basic_event',
// repeat: 2
// },
// {
// // Weekday event
// title: 'Click for Google',
// url: 'http://google.com/',
// start: '2017-02-28',
// className: 'scheduler_basic_event',
// dow: [1,5]
// }
// ];

// // Any value represanting monthly repeat flag
// var REPEAT_MONTHLY = 1;
// // Any value represanting yearly repeat flag
// var REPEAT_YEARLY = 2;

// $('#calendar').fullCalendar({
// editable: true,
// defaultDate: new Date(),
// eventSources: [defaultEvents],
// dayRender: function( date, cell ) {
// // Get all events
// var events = $('#calendar').fullCalendar('clientEvents').length ? $('#calendar').fullCalendar('clientEvents') : defaultEvents;
// // Start of a day timestamp
// var dateTimestamp = date.hour(0).minutes(0);
// var recurringEvents = new Array();

// // find all events with monthly repeating flag, having id, repeating at that day few months ago  
// var monthlyEvents = [];
// monthlyEvents = events.filter(function (event) {
// return event.repeat === REPEAT_MONTHLY &&
// event.id &&
// moment(event.start).hour(0).minutes(0).diff(dateTimestamp, 'months', true) % 1 == 0
// });

// // find all events with monthly repeating flag, having id, repeating at that day few years ago  
// var yearlyEvents = [];
// yearlyEvents = events.filter(function (event) {
// return event.repeat === REPEAT_YEARLY &&
// event.id &&
// moment(event.start).hour(0).minutes(0).diff(dateTimestamp, 'years', true) % 1 == 0
// });


// recurringEvents = monthlyEvents.concat(yearlyEvents);

// $.each(recurringEvents, function(key, event) {
// var timeStart = moment(event.start);

// // Refething event fields for event rendering 
// var eventData = {
// id: event.id,
// allDay: event.allDay,
// title: event.title,
// description: event.description,
// start: date.hour(timeStart.hour()).minutes(timeStart.minutes()).format("YYYY-MM-DD"),
// end: event.end ? event.end.format("YYYY-MM-DD") : "",
// url: event.url,
// className: 'scheduler_basic_event',
// repeat: event.repeat
// };

// });

// }
// });
// </script> -->
