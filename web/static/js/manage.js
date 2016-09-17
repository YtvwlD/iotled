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
				$("<tr></tr>")
					.append($("<td></td>")
						.html(device)
					)
					.appendTo("#devices-list");
			});
		},
		error: function(xhr, status, errorThrown)
		{
			alert("Sorry, there was a problem.");
			console.log("Error: " + errorThrown);
			console.log("Status: " + status);
			console.dir(xhr);
		}
	});
}

listDevices();
