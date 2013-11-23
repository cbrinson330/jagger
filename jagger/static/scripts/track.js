(function(jag, $){
	
	var url = '/api/interest/getValues',
			seriesValues = [];

	$.ajax({
		url: url,
		success: function(data){
			console.log('youve scceeded... I hope youre happy');
			console.log(data);
			jag.parseJson(data);
		},
		failure: function(data){
			console.log('youve failed... I hope youre happy');
			console.log(data);
		}
	});

	jag.parseJson = function(rawJson){
		var cleanJson = [];
		for (var key in rawJson) {
  		var obj = rawJson[key],
					seriesObject = {};
			seriesObject.name = obj.name;
			seriesObject.data = [];

  		for (var prop in obj.dateVals) {
				var localDateVals = obj.dateVals[prop],
						year = parseInt(localDateVals.year),
						month = parseInt(localDateVals.month),
						day = parseInt(localDateVals.day),
						value = parseInt(localDateVals.value),
						validDate = [Date.UTC(year,month,day),value];
						//validDate = [year+month+day,value];
			
				seriesObject.data.push(validDate);
  		}
			cleanJson.push(seriesObject);
		}
		console.log(cleanJson);

		$('#chart').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Your motivation'
        },
        xAxis: {
            type: 'date',
            dateTimeLabelFormats: { // don't display the dummy year
								day: '%e. %b',
                month: '%b \'%y',
                year: '%Y'
            }
        },
        yAxis: {
            title: {
                text: 'Level of motivation'
            },
            min: 0
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y +' m';
            }
        },
        
        series: cleanJson
    });	
	}

})(window.jagger.track = window.jagger.track || {}, $);
