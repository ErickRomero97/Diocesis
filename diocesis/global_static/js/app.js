$(function(){
	$('.btnEditar').on('click', function(e){
		e.preventDefault();

		id = $(this).attr('data-id');
		url = $(this).attr('data-url');
		
		$.get(url, {'idPub': id}, function(data){
			$('#id_pub').val(id);
			$('#id_nombre').val(data.nombre);
			$('#id_contenido').val(data.contenido);
			$('#id_empleado').val(data.empleado);
			$('#id_fecha').val(data.fecha);
		})
	})

	$('#confirm-delete').on('show.bs.modal', function(e) {
		$(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
		$('.debug-url').html('Delete URL: <strong>' + $(this).find('.btn-ok').attr('href') + '</strong>');
	});

	// AL iniciar la pagina cargue las homilias del combobox inicial

	fecha = new Date();

	url = $('#cboMes').attr('data-url');

	$.get(url, {'id': fecha.getMonth() + 1}, function(data){
		$('#datosHomilia').empty();
		$('#datosHomilia').append(data.format);
		$('#mes').text(mesEnPalabras(fecha.getMonth()));
	})

	$('#cboMes').change(function(){
		id = $(this).val();
		url = $(this).attr('data-url');

		$.get(url, {'id': id}, function(data){
			$('#datosHomilia').empty();
			$('#datosHomilia').append(data.format);
			$('#mensaje').text(data.msj);
			$('#mes').text(mesEnPalabras(id - 1));
		})
	})

	function mesEnPalabras(numMes){
		fecha = new Date();
		mes = '';

		if ((numMes + 1) == 1){
			mes = 'Enero';
		}else if((numMes + 1) == 2){
			mes = 'Febrero';
		}else if((numMes + 1) == 3){
			mes = 'Marzo';
		}else if((numMes + 1) == 4){
			mes = 'Abril';
		}else if((numMes + 1) == 5){
			mes = 'Mayo';
		}else if((numMes + 1) == 6){
			mes = 'Junio';
		}else if((numMes + 1) == 7){
			mes = 'Julio';
		}else if((numMes + 1) == 8){
			mes = 'Agosto';
		}else if((numMes + 1) == 9){
			mes = 'Septiembre';
		}else if((numMes + 1) == 10){
			mes = 'Octubre';
		}else if((numMes + 1) == 11){
			mes = 'Noviembre';
		}else {
			mes = 'Diciembre';
		}

		return mes;
	}

	$(document).on('click', '.btnEditarHomilia', function(e){
		e.preventDefault();
		
		id = $(this).attr('data-id');
		url = $(this).attr('data-url');

		$.get(url, {'id': id}, function(data){
			$('#id_homilia').val(id);
			$('#id_titulo').val(data.titulo);
			$('#id_parroquia').val(data.parroquia);
			$('#id_fecha').val(data.fecha);
			$('#id_hora').val(data.hora);
			$('#id_empleado').val(data.empleado);
			$('#id_contenido').val(data.contenido);
		})
	})
})