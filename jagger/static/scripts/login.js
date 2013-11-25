(function(jag, $){
	$("form").submit(function(e){
		var $that = $(this),
		 		username = $that.find('.username').val(),
				pass = $that.find('.pass').val(),
				email = $that.find('.email').val(),
				url = '',
				$error = $('.error');

		if($that.hasClass('login-form')){
			url = '/api/interest/login';
		}
		else if($that.hasClass('register-form')){
			url = '/api/interest/register';
		}
		else{
			return false;
		}
		url += '?username='+username+'&password='+pass+'&email='+email;
		
		$.ajax({
			url: url,
			success:function(data){
				console.log(data);
				if(data.code != '500'){
					window.location = 'http://localhost:8000/track';
				}
				else{
					$error.fadeOut().text(data.error).fadeIn(250);
					return false;
				}
			},
			failure:function(data){
				console.log(data);
			}
		});
		e.preventDefault();
	});
})(window.jagger.login = window.jagger.login || {}, $);
