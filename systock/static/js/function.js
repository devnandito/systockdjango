$(document).on("ready", inicio);
function inicio()
{
	$("label[for='user'] input[type=text]").attr("placeholder", "Usuario");
	$("label[for='pass'] input[type=password]").attr("placeholder", "Contraseña");
	$("label[for='error']").addClass("error");
	$('.add').on('click', clone);
	$('#displayblock').on('click','.close', delclone);
	var days=[ "D", "L", "M", "X", "J", "V", "S" ];
	var months=[ "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" ];
	$('#fecha input').datepicker({dayNamesMin: days , dateFormat: "yy-mm-dd", monthNames: months});
	/*$('#fecha input').datepicker({dateFormat: 'yy-mm-dd'});*/
	/*$('.orden ul li').hide();
	$('.orden ul').hover(showorden);*/
	/*$("label[for='pwd1'] input[type=password]").attr("placeholder", "Contraseña");
	$("label[for='pwd2'] input[type=password]").attr("placeholder", "Repita la Contraseña");*/
	/*$("input[type=checkbox]").on("click", marcar);
	$("input[type=checkbox]").attr("disabled", "disabled");*/
	/*$("#mail").attr("placeholder", "Correo electronico");
	$("label[for='usr'] input[type=text]").attr("placeholder", "Usuario");*/
	/*$("#search").change(searchs);*/
}
/*function showorden()
{
	$('.orden ul li').toggle();
}*/
var clickedcount = 1;
function clone()
{
	$('#mainDiv').clone().attr('id', 'mainDiv'+clickedcount).appendTo('#displayblock');
	$('<span>',{class:'close', text:'Borrar'}).appendTo('#mainDiv'+clickedcount+' table td:last');
	clickedcount++;
}
function delclone()
{
	$('#displayblock div:last').slideUp('slow', del);
}
function del()
{
	$(this).remove();
}
/*function marcar()
{
	if ($(this).is(":checked"))
	{
		var group = "input:checkbox[name='"+$(this).attr("name")+"']";
		$(group).prop("checked", false);
		$(this).prop("checked", true);
	}
	else
	{
		$(this).prop("checked", false);
	}
}*/
/*function searchs()
{
	$.ajax({
		type: "GET",
		url: "/search",
		data: 
			{
				search_text: $("#search").val(),
				csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()
			},
		success: resultado,
		dataType: "html"
	});
}*/
/*function mostrar(url)
{
	$.ajax({
		url: url,
		type: "GET",
		success: resultado
	});
}
function resultado(data)
{
	$("#resultado").html(data);
}*/
/*function insert(url, id)
{
	var v1 = $(id).serialize();
	$.ajax({
		url: url,
		type: "POST",
		data: v1,
		success: resultado
	});
}*/
//var v1=$(id).serialize();
/*function marcar()
{
	if ($(this).is(":checked"))
	{
		var group = "input:checkbox[name='"+$(this).attr("name")+"']";
		$(group).prop("checked", false);
		$(this).prop("checked", true);
	}
	else
	{
		$(this).prop("checked", false);
	} 
}*/

