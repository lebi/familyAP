var nowdate;
var event_action;
var eventId;
$(document).ready(function() {
	$("#collapse a").each(function () {
		// body...
		$(this).click(function () {
			// body...
			$(this).parent().parent().parent().find("li").removeClass("active");
			$(this).parent().addClass("active");
			if (document.body.clientWidth<=751)
				$("#collapse").collapse('toggle');
			// console.log(document.body.clientWidth);
		})
	})

	$("#s-date").datetimepicker();
  getEventDate();
  var today=moment().format('YYYY-MM-DD');
  nowdate=today;
  getEventList(today);
  $("#modal-submit").click(function(){
    var url=event_action;
    console.log(url);
  })

});


function Event(title,date,datetime,content) {
  this.title=title;
  this.date=date;
  this.datetime=datetime;
  this.content=content;
}


function Event(event) {
  this.title=event.title;
  this.date=event.date;
  this.datetime=event.datetime;
  this.content=event.content;
  this.id=event.id;
}


function EventDate(date) {
  this.date=date;
}

function getEventDate() {
  // body...
  var url='/guest/eventdate';
  $.getJSON(url,function (result) {
    if(result.status>0){
      var eventArray=new Array();
      for (var i = 0; i < result.data.length; i++) {
        eventArray[i]=new EventDate(result.data[i].date);
      }
      render_schedule(eventArray);
    }
  })
}

function render_schedule(eventArray){
	var calendars = {};
  var thisMonth = moment().format('YYYY-MM');
	calendars.clndr2 = $('#scheduleWrap').clndr({  
    daysOfTheWeek: ['Sun', 'Mon', 'Tus', 'Wen', 'Thu', 'Fri', 'Sat'],
    template: $('#template-calendar').html(),
    events: eventArray,
    multiDayEvents: {
      startDate: 'startDate',
      endDate: 'endDate',
      singleDay: 'date'
    },
    startWithMonth: moment(),
    clickEvents: {
      click: function(target) {
        nowdate=target.date._i;
        console.log(nowdate);
        getEventList(target.date._i);
      }
    },
    forceSixRows: true
  });  
  $('#scheduleWrap .clndr-grid .days .day').click(function(){
    $('#scheduleWrap .chosen').removeClass('chosen');
    $(this).addClass('chosen');
  });

  $("#scheduleWrap .event-listing-add").click(function () {
    console.log('add');
    addEvent();
  })
}

function getEventList(date){
  var url='/guest/eventlist?date='+date;
  $.getJSON(url,function (result) {
    if(result.status>0){
      var eventList=new Array();
      for (var i = 0; i < result.data.length; i++) {
        var event=new Event(result.data[i]);
        eventList[i]=event;
      };
      render_event(eventList);
    }
  })
}

function render_event(eventList){
  console.log(eventList);
  $('.event-row').remove();
  var temp=_.template($('#template-event').html());
  $('.event-listing').append(temp({eventList:eventList}));
  
  $("#scheduleWrap .edit-icon").click(function () {
    updateEvent(this);
  })

  $("#scheduleWrap .remove-icon").click(function () {
    deleteEvent(this);
  })
}

function addEvent() {
  $('#s-modal input').val('');
  $('#s-modal textarea').val('');
  event_action="eventadd";
  $('#s-modal').modal('show');
}

function updateEvent(dom){
  var datetime=$(dom).parent().parent().find('.event-item-name').text();
  var content=$(dom).parent().parent().find('.event-item-location').text();
  eventId=$(dom).parent().attr('eid');
  console.log(eventId);

  $('#s-modal input').val(datetime);
  $('#s-modal textarea').val(content);
  event_action="eventupdate";
  $('#s-modal').modal('show');
}

function postEvent(){
  var time=$('#s-modal input[name=time]').val();
  var content=$('#s-modal textarea').val();
  content=encodeURIComponent(content);
  $.post(event_action,{eventId:eventId,date:nowdate,time:time,content:content},function(result) {
    if (result.status>0) {
      $('#s-modal').modal('toggle');
      getEventList(nowdate);
    };
  })
}

function deleteEvent(dom) {
  var eid=$(dom).parent().attr('eid');
  $.getJSON("eventdelete",{eventId:eid},function(result){
    if(result.status>0){
      getEventList(nowdate);
    }
  })
}