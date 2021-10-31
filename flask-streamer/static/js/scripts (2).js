/*!
* Start Bootstrap - Coming Soon v6.0.5 (https://startbootstrap.com/theme/coming-soon)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-coming-soon/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function redirect() {
	alert("its working");
  	location.href = "https://www.w3schools.com";
}

function validate_url(url_input){
	var regexquery = "^(https?://)?(((www\\.)?([-a-z0-9]{1,63}\\.)*?[a-z0-9][-a-z‌​0-9]{0,61}[a-z0-9]\\‌​.[a-z]{2,6})|((\\d{1‌​,3}\\.){3}\\d{1,3}))‌​(:\\d{2,4})?(/[-\\w@‌​\\+\\.~#\\?&/=%]*)?$‌​";
	var url = new RegExp(regexquery, "i");
	return url.test(url_input);
}


