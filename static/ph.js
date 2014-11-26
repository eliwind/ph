// Initialization on page load
$(document).ready(function() {
	
    // set up the calendar
    $('#calendar').fullCalendar({
        weekends: false,
        events: '/schedule',

        // handle event clicks: pop up edit box
        eventClick: function(calEvent, jsEvent, view) {

            // set up shift variables for the popup
            if (calEvent.worker) {
                $('#shiftTitle').text("Change Shift Assignment");
                $('#shiftWorker').val(calEvent.worker.name);
                $('#shiftEmail').val(calEvent.worker.email);
                $('#shiftFamily').val(calEvent.worker.family);
                $('#cancelShift').show();
            } else {
                $('#shiftTitle').text("Parent Help Signup");
                $('#shiftWorker').val("");
                $('#shiftEmail').val("");
                $('#shiftFamily').val("");
                $('#cancelShift').hide();

            }
			dateStr = calEvent.start.toLocaleDateString();
			shift = calEvent.shift;
			if (shift.indexOf('AM') == 0) {
				startTime = '8:30:00 AM';
				endTime = '1:00 PM';
			} else if (shift == 'PM') {
				startTime = '12:30 PM';
				endTime = '2:30 PM';
			} else if (shift == 'Snack') {
				startTime = '8:30:00 AM';
				endTime = '9:00:00 AM';
			}

			$('#calStart').text(dateStr + ' ' + startTime);
			$('#calEnd').text(dateStr + ' ' + endTime);
			$('#calSummary').text('Parent Help');
			$('#calDesc').text('Parent Help at Agassiz Preschool')
			addthisevent.refresh();
			
            $('#shiftDate').val(dateStr);
            $('#shift').val(shift);
            $('#errMsg').hide();

            displayPopup ('#popup')

            // stash the calendar even that was clicked
            $('#popup').data('event', calEvent);
        }
    });

    // Handle 'find shifts' link
    $('#findLink').click(function() {

        $('#shiftDiv').hide();
        $('#findFamily').val('');
        displayPopup ('#find');
        return false;
    });

	getConfig();
	
	
    // Handle 'setup' link
    $('#setupLink').click(function() {
		var cfg = $('#setup').data('config');
		$('#phcName').val(cfg.phcName);
		$('#phcEmail').val(cfg.phcEmail);
		$('#phcPhone').val(cfg.phcPhone);
        displayPopup ('#setup');
        return false;
    });


    $('#newSemesterLink').click(function() {
		$('#semesterStart').val('');
		$('#semesterEnd').val('');
		$('#semesterHolidays').val('');
		$('#semesterHalfDays').val('');
        displayPopup ('#newSemester');
        return false;
    });
	

	
    // Close popup
    $('#closePopup').click(function() {closePopup('#popup')});

    // Close popup
    $('#closeFind').click(function() {closePopup('#find')});

    // Close popup
    $('#closeSetup').click(function() {closePopup('#setup')});

    // Close popup
    $('#closeSemester').click(function() {closePopup('#newSemester')});

    // Save a shift
    $('#saveShift').click(function(){
        signup ($('#popup').data('event'));
    });

    // Cancel a shift
    $('#cancelShift').click(function(){
        var event = $('#popup').data('event');
        if (confirm ("Really, really cancel " + $('#shiftWorker').val() + "'s shift?  There's not an easy way to undo this.")) {
            cancel (event.start, event.shift);
        }
    });

    // Find shifts
    $('#findShift').click(function(){
        $.ajax({
            url: '/shifts',
            dataType: 'json',
            data: {
                family: $('#findFamily').val()
            },
            success: showShifts,
            error: function(xhr, status, error) {
                alert ('Error.  Try again in a minute or two');
            }
			
        });
    });

    // Save setup
    $('#saveSetup').click(function() {
        $.ajax({
            url: '/config',
            dataType: 'json',
			type: 'POST',
            data: {
				phcName: $('#phcName').val(),
				phcEmail: $('#phcEmail').val(),
				phcPhone: $('#phcPhone').val()
            },
            success: function (result, status, xhr) {
				getConfig();
				closePopup('#setup');
			},
            error: function(xhr, status, error) {
                alert ('Error.  Try again in a minute or two');
            }
			
        });
    });

	// Add a semester
    $('#saveSemester').click(function() {
        $.ajax({
            url: '/load_semester',
            dataType: 'json',
            data: {
				start: $('#semesterStart').val(),
				end: $('#semesterEnd').val(),
				holidays: $('#semesterHolidays').val().split(','),
				half_days: $('#semesterHalfDays').val().split(',')
            },
	    traditional: true,
            success: function (result, status, xhr) {
				$('#calendar').fullCalendar('refetchEvents');
				closePopup('#newSemester');
			},
            error: function(xhr, status, error) {
                alert ('Error.  Try again in a minute or two');
            }
			
        });
    });
	
});

function getConfig() {
	$.ajax({
        url: '/config',
        dataType: 'json',
        success: function(result, status, xhr) {
			$('#setup').data('config', result);
		}		
    });
}

function displayPopup(dlg) {
    $('#overlay, ' + dlg).animate({'opacity':'0.7'}, 300, 'linear');
    $(dlg).animate({'opacity':'1.00'},300,'linear');
    $('#overlay, ' + dlg).css('display','block');
    $(dlg).css({'left':(($(window).width()/2)-($(dlg).width()/2))});
    $(dlg).css({'top':(($(window).height()/2)-($(dlg).height()/2)-50)});
}


function closePopup(dlg) {
    $('#overlay, ' + dlg).animate({'opacity':'0'},300,'linear', function(){
        $('#overlay, ' + dlg).css('display','none');
    });
}

function signup (event) {
    var date = event.start;
    var shift = event.shift;
    var name = $('#shiftWorker').val();
    var email = $('#shiftEmail').val();
    var family = $('#shiftFamily').val();
	
    if (!name || !email || !family) {
        $('#errMsg').text('Fill out form completely. All fields are required.');
        $('#errMsg').show();
        return;
    }
    $.ajax({
        url: '/signup',
        dataType: 'json',
        data: {
            date: date.toISOString().slice(0,10).replace(/-/g,""),
            shift: shift,
            name: name,
            email: email,
            family: family
        },
        success: function(result, status, xhr) {
            $('#calendar').fullCalendar('refetchEvents');
            closePopup('#popup');
			
        },
        error: function(xhr, status, error) {
            alert ('Error signing up.  Try again in a minute or two.');
        }
		
    });
}

function cancel (date, shift) {
        $.ajax({
                    url: '/cancel',
                    dataType: 'json',
                    data: {
                        date: date.toISOString().slice(0,10).replace(/-/g,""),
                        shift: shift
                    },
                    success: function(result, status, xhr) {
                        $('#calendar').fullCalendar('refetchEvents');
                        closePopup('#popup');

                    },
                    error: function(xhr, status, error) {
                        alert ('Error canceling shift.  Try again in a minute or two.');
                    }

                });
}

function showShifts (result, status, xhr) {
    // clear out table
    $('#shiftData').empty();

    // sort shifts by date, then by shift name
    var shiftComparator = function (a, b) {
        var result = a['date'].localeCompare(b['date']);
        if (result == 0) {
            result = a['shift'].localeCompare(b['shift']);
        }
        return result;
    }

    if (result.length > 0) {
        // add shifts to the table
        result.sort (shiftComparator).forEach (function (shift) {
                      shiftDate = new Date(shift['date']);
                      $('#shiftData').append('<tr><td>' + (shiftDate.getUTCMonth() + 1) + '/' + shiftDate.getUTCDate() + '/' + shiftDate.getUTCFullYear() +
    							  '</td><td>' + shift['worker']['name'] +
    						        '</td><td>' + shift['shift'] + '</td></tr>');                            
                  });
        $('#shiftTable').show();
        $('#noneFound').hide();
    } else {
        $('#shiftTable').hide();
        $('#noneFound').show();
    }
    $('#shiftDiv').show();
}
