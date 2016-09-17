"use strict";

var devices = [];

function listDevices()
{
	$.ajax({
		url: "/api/app/list",
		type: "GET",
		dataType: "json",
		success: function (json)
		{
			json.forEach(function(device)
			{
				devices.push(device);
				$.ajax({
					url: "/api/app/" + device,
					type: "GET",
					dataType: "json",
					success: function(json)
					{
						$("<tr></tr>")
							.append($("<td></td>")
								.html(device)
							)
							.append($("<td></td>")
								.html(json)
							)
							.appendTo("#devices-list");
					},
					error: handleError
				});
			});
		},
		error: handleError
	});
}

function turnOn(device, led)
{
	$.ajax({
		url: "/api/app/" + device,
		type: "POST",
		data: {
			command: "turn_on",
			params: '["' + led + '"]'
		},
		error: handleError
	});
}

function turnOff(device, led)
{
	$.ajax({
		url: "/api/app/" + device,
		type: "POST",
		data: {
			command: "turn_off",
			params: '["' + led '"]'
		},
		error: handleError
	});
}

function handleError(xhr, status, errorThrown)
{
	alert("Sorry, there was a problem.");
	console.log("Error: " + errorThrown);
	console.log("Status: " + status);
	console.dir(xhr);
}

listDevices();
