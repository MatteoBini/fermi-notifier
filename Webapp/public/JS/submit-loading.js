function loading(){
	var submitBtn = document.getElementById("submit-btn");
	var width = window.getComputedStyle(submitBtn).getPropertyValue('width');
	var height = window.getComputedStyle(submitBtn).getPropertyValue('height');
	submitBtn.style.width = width;
	submitBtn.style.height = height;
	submitBtn.innerHTML = "<img src='/IMG/loading.png' class='submit-loading rotate-loading'>";
}