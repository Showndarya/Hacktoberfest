var users = []
var i = 0;

var getData = (function($){
	var URL = "https://api.github.com/repos/Showndarya/Hacktoberfest/commits?per_page=100"
	
	$.get(URL,function(data,status) {

			data.forEach(function(d) {
				
				if(d.author==null){
					return true;
				}
				
				if(users.indexOf(d.commit.author.email) == -1) {

				    var mes = d.commit.message;
				    var name = d.commit.author.name;
				    
				    if(name == ""){
					    name = mes;
				    }
				    
				    var template = 
				    "<div class='col-md-3 col-xs-6 col-lg-3' id='author'><div class='container-fluid'>" +
					    "<a class='thumbnail' target='_blank' href='" + d.author.html_url + "'>" + 
						    "<img src='" + d.author.avatar_url + "' alt='' class='img-responsive'>" +  
					    "</a>" +
					    "<div class='caption'>" +
						    "<strong>" + d.author.login + "</strong>" +
						    "<p>" + name + "</p>"+
					    "</div></div></div>" 
					    
			        $('#contributors').append(template);
			        users[i] = d.commit.author.email;
			        i=i+1;
                }
                
			});
			
	});


})($);
