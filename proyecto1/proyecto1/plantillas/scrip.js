
var imagen=new Array(3);

function saludo(){
	alert("que pasa?");
	}

function ejecuta(){
	//document.getElementsByTagName("p")[0].onclick=saludo;//seleciona la primer([0]) etiqueta <p>
	//document.getElementsByTagName("#cabeceraweb")[0].onclick=saludo;
	document.getElementsByTagName("#cabeceraweb")[0].onclick=saludo;
	}


function gestor(){
	for(var i=0;i<4;i++){
		imagen[i]=document.getElementsByTagName("img")[i];
		}
	
	/*imagen[0].addEventListener("mouseover",function(){imagen[0].width=420;imagen[0].height=280;},false);
	imagen[0].addEventListener("mouseout",function(){imagen[0].width=320;imagen[0].height=180;},false);
	
	imagen[1].addEventListener("mouseover",function(){imagen[1].width=420;imagen[1].height=280;},false);
	imagen[1].addEventListener("mouseout",function(){imagen[1].width=320;imagen[1].height=180;},false);
	
	imagen[2].addEventListener("mouseover",function(){imagen[2].width=420;imagen[2].height=280;},false);
	imagen[2].addEventListener("mouseout",function(){imagen[2].width=320;imagen[2].height=180;},false);
	
	imagen[3].addEventListener("mouseover",function(){imagen[3].width=420;imagen[3].height=280;},false);
	imagen[3].addEventListener("mouseout",function(){imagen[3].width=320;imagen[3].height=180;},false);	*/
	}
	
/*function crecer(){
	imagen.width=420;
	imagen.height=280;
	}*/

/*function decrecer(){
	imagen.width=320;
	imagen.height=180;
	
	}*/
window.onload=gestor;
//al cargar veentana ejecuta saludo
