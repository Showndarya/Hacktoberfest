var users = []
var i = 0

var getData = (function ($) {
  var URL = 'https://api.github.com/repos/Showndarya/Hacktoberfest/contributors'

  $.get(URL, function (data, status) {
    data.forEach(function (d) {
      if (d.login == null) {
        return true
      }

      if (users.indexOf(d.url) == -1) {
	    var template =
	    "<div class='col-md-3 col-xs-6 col-lg-3' id='author'><div class='container-fluid'>" +
		    "<a class='thumbnail' target='_blank' href='" + d.html_url + "'>" +
			    "<img src='" + d.avatar_url + "' alt='' class='img-responsive'>" +
		    '</a>' +
		    "<div class='caption'>" +
			    '<strong>' + d.login + '</strong>' +
			    '<p> Contributions: ' + d.contributions + '</p>' +
		    '</div></div></div>'

        $('#contributors').append(template)
        users[i] = d.url
        i = i + 1
      }
    })
  })
})($)
