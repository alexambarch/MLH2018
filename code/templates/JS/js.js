function boot(){
	var dict = {'a':false, 'b':false, 'c':false, 'd':false, 'e':false, 'f':false, 'g':false, 'h':false, 'i':false, 'j':false, 'k':false, 'l':false, 'm':false, 'n':false};
	var keys = Object.keys(dict);
	//get the api shit here
	for(var i in keys){
		var list = dict[i];
		var car = list[0];
		var x = list[0];
		var y = list[1];
		if((x1<x)&(x<x2)&(y1<y)&(y<y2)){
			document.getElementById(spot).style.backgroundColor = "green";
		}
		else{
			document.getElementById(spot).style.backgroundColor = "red";
		}
	}
}

function hello(){
	console.log('hello');
}