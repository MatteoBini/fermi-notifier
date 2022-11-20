var submitBtn = document.getElementById("submit-btn");
var width = window.getComputedStyle(submitBtn).getPropertyValue('width');
var height = window.getComputedStyle(submitBtn).getPropertyValue('height');
submitBtn.style.width = width;
submitBtn.style.height = height;

function ShowPSW() {
	var id = document.getElementById("password");
	if (id.type === "password") {
		id.type = "text";
		document.getElementById("PSWShowHideIcon").innerHTML = '<i class="fa-solid fa-eye"></i>';
	} else {
		id.type = "password";
		document.getElementById("PSWShowHideIcon").innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
	}
}

// edge automatically adds the show/hide password button, wtf edge
var browser = (function (agent) {
	if(agent.indexOf("edg/") > -1){
		document.getElementById("PSWShowHideIcon").style.display = "none";
	}
})(window.navigator.userAgent.toLowerCase());