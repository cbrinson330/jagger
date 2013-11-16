(function(jag, $){
	
	jag.clearFields = function(){
		$('#name').val('');
		$('#maxVal').val('');
		$('#minVal').val('');
	}

	jag.removeItem = function(id){
		$("li[data-id='"+id+"']").remove();
	}
	
	jag.addItem = function(name, id){
		$('.interestList').append('<li data-id="'+id+'">'+name+'<span class="delete">X</span></li>');
	}

	$('.interestList').on('click','li .delete', function(){
		console.log('test');
		var id = $(this).parents('li').data("id"),
				url = '/api/interest/delete/?id='+id;

		$.ajax({
			url:url,
			success: function(data){
				console.log(data);
				jag.removeItem(data.content.id);
			}
		});
	});

	$("#submitInterest").click(function(e){
		var newName = $('#name').val();
		var newMaxVal = $('#maxVal').val();
		var newMinVal = $('#minVal').val();
		
		if(newName != "" && newMaxVal != "" && newMinVal != ""){
			//submit the form
			var url='/api/interest/create/?name='+newName+'&maxVal='+newMaxVal+'&minVal='+newMinVal;
			
			$.ajax({
				url:url,
				success:function(data){
					console.log(data);
					if(data != ""){
						$('.success').fadeOut().fadeIn(250);
						jag.clearFields();
						jag.addItem(data.name, data.id);
					}
				}
			});
		}
		else{
			$(".error").hide().fadeIn(250);
		}
		return false;
	}); 
	
})(window.jagger.create = window.jagger.create || {}, $);
