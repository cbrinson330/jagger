(function(jag, $){
	var inputVals=[],
			domList = $('.items li').length,
			$error = $('.error'),
			$success = $('.success');
			
	
	$('.knob').knob({
		'release':function(v){
			var item = [],
					interestId = this.$.parents('li').data('id'),
					$error = $('.error');

			item.push(interestId);
			item.push(v);
			inputVals.push(item);
		}
	});

	$('#save-btn').click(function(e){
		if(domList === inputVals.length){
			var url = '/api/interest/update/?';
			for(i=0; i<inputVals.length; i++){
				url +='value'+i+'='+inputVals[i][0]+':'+inputVals[i][1]+'&';
			} 
			
			$.ajax({
				url: url,
				success: function(data){
					if(data.code == 500){
						$error.hide().text('You already entered values today.').fadeIn(250);
					}
					else{
						$error.hide();
						$success.show();
					}
				}
			});
		}
		else{
			$error.hide().text('Fill in values for all interests.').fadeIn(250);
		}
		e.preventDefault();
	});
	
})(window.jagger.enter = window.jagger.enter || {}, $);
