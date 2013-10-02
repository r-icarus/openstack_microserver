/* Additional JavaScript for microserver. */

window.setInterval(function(){
	getUpdatedServerStatus();
},60000);

var getUpdatedServerStatus = function(){
	$("[id^=recipes__row__]").each( function(){
		$(this).delay(1500);
		var idTd = $(this).find('td').eq(1);
		var serverId = idTd.text();
		var that = $(this);
		$.getJSON("/microserver/server_status/"+serverId, function(data){
			var serverStatus = data['status'];
			var statusTd = that.find('td').eq(5);
			statusTd.text(serverStatus);
		});
	});
}