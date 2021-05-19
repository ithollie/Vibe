window.onload = function(){
	var myApp =  angular.module('myApp', []);

	var id_name = document.getElementById("header");
	var mainColor = document.getElementById("main");
	var Color =  "gray";
	var h1color = "red";
	var ang = function($scope,Data){

	}
	var bigtime = function(){
		var Anrray = new Array()
		var vinish = document.getElementById("header");
		if(vinish){
			Anrray = vinish;
		}
		return Anrray;
	}
	var openwindow = function(header){
		//window.open('c://users/hacker/desktop/startup/machine/templates/login.html');
		
	}

	var buttom = function(id_name,color,h1color){
		var gu  = id_name.style.color = h1color;
		var id = id_name.style.background = color; 
	}

	openwindow(id_name);
	buttom(id_name,Color,h1color);
	console.log(bigtime());
}

