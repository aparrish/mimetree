window.onload = function(){

		$.getJSON('/baby.json', function(data) {
			//console.log(data);
var dataString = '
	<div id="BreedResults">
			<div class="BabyName"><p>'+data["baby"]["first_name"]+" "+data["baby"]["last_name"]+'</p></div>
			<div id="BabyContainer">';
			var images = data["images"];
			for(var j=images.length-1;j>=0;j--){
				var ind = j+1;
				dataString += '<img src="'+images[j]+'" style="z-index:'+ind+'">';
			}
			</div>
			<div class="BabyData">
				<br>
				<div id="BabyDesc">
					<p style="padding-left:3px">The fate of the world is in your hands, and your friends' loins!</p>
				</div>
				<div class="clear"></div>
				<br>
				<div id="BabyStats" style="padding-bottom:0px">
					<br>
				</div>
			</div>
			<div class="clear"></div>
		</div>			
			 dataString += ;
			$(dataString).appendTo("#BabyName");
			
			dataString = '<p>'+data["bio"]+'</p>';
			$(dataString).appendTo("#BabyDesc");
			

			dataString = '<table style="margin-left:3px">';
					dataString += '<tr><td><strong>Proficiency</strong></td><td>'+data["baby"]["stats"]["proficiency"]+'</td></tr>';
					dataString += '<tr><td><strong>Enthusiasm</strong></td><td>'+data["baby"]["stats"]["enthusiasm"]+'</td></tr>';
					dataString += '<tr><td><strong>Usefulness</strong></td><td>'+data["baby"]["stats"]["usefulness"]+'</td></tr>';
					dataString += '<tr><td><strong>Intrugue</strong></td><td>'+data["baby"]["stats"]["intrigue"]+'</td></tr>';
					dataString += '<tr><td><strong>Literacy</strong></td><td>'+data["baby"]["stats"]["literacy"]+'</td></tr>';
					dataString += '<tr><td><strong>Privacy</strong></td><td>'+data["baby"]["stats"]["privacy"]+'</td></tr>';
					dataString+='</table>';

		});
		
		//CreateDragContainer(document.getElementById('DragContainer7'));
		//CreateDragContainer(document.getElementById('DragContainer8'));
	
}