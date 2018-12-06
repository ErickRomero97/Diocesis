$(function(){
	
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
			$('#mensaje').html(data.msj);
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


	// //desactivar el obispo actual
	// $('#btn_dObispo').on('click', function(){
	// 	var id = $(this).attr('data-id');
	// 	var url = $(this).attr('data-url');
	// 	var btn=$(this);
	// 	$.get(url, {'id':id},function(data){
	// 		$(btn).html(data.action);
	// 		$('#data_Obispo').fadeOut();
	// 		$('#nuevo_Obispo').fadeIn();


	// 	}, 'json');

	// });

	var _ID = 0;
	$(document).on('click', '.btn_pastoral', function(){
			_ID = $(this).attr('data-id');
	})
	//eliminar pastoral
	$('#btn_dPastoral').on('click', function(){
		

		var url = $(this).attr('data-url');
		var btn=$(this);
		$.get(url, {'id':_ID},function(data){
			$('#data_Pastoral-'+_ID).fadeOut()
		}, 'json');

	});


	//activar usuarios del sistema
	$('.btn-user').on('click', function(){
		var id = $(this).attr('data-id');
		var url = $(this).attr('data-url');
		var btn=$(this);
		$.get(url, {'id':id},function(data){
			$(btn).html(data.action);
			$('#estado-' + id).text(data.valor);
			if (data.action == 'Activar'){
				$(btn).removeClass('btn btn-danger');
				$(btn).addClass('btn btn-success');
			}else{
				$(btn).removeClass('btn btn-success');
				$(btn).addClass('btn btn-danger');
			}		
		}, 'json');

	});

	//Agregar Usuarios al sistema
	$('#frmUsuario').on('submit', function(e){
		if ($(this).attr('data-id').toString().trim() ==''){
			e.preventDefault();

			var url = $(this).attr('action');

			$.post(url, $(this).serialize(), function(data){
				$('#add_usuario').append(data.response);
				$('#id_username').val('').focus();
				$('#id_password1').val('');
				$('#id_password2').val('');
			}, 'json');
		}
	});


	//agregar empleados al sistema
	$('#frmEmpleado').on('submit', function(e){
		if ($(this).attr('data-id').toString().trim() ==''){
			e.preventDefault();
			var url = $(this).attr('action');
			var data = new FormData($('#frmEmpleado').get(0));

			$.ajax({
				url: url,
				type: $(this).attr('method'),
				data: data,
				cache: false,
				processData: false,
				contentType: false,
				success: function(data) {
				    $('#add_empleado').append(data.response);
					$('#id_numero_identidad').val('').focus();
					$('#id_nombre').val('');
					$('#id_apellido').val('');
					$('#id_fecha_nac').val('');
					$('#id_fecha_ord').val('');
					$('#id_telefono').val('');
					$('#id_direccion').val('');
					$('#id_biografia').val('');
					$('#id_correo').val('');
					$('#id_imagen').val('');
					$('#id_sexo').val('');
					$('#id_cargo').val('');
					$('#id_user').val('');
				}
			});
		}
		
	});

	//activar empleados del sistema
	$('.btn-empleado').on('click', function(){
		var id = $(this).attr('data-id');
		var url = $(this).attr('data-url');
		var btn=$(this);
		$.get(url, {'id':id},function(data){
			$(btn).html(data.action);
			$('#estado-' + id).text(data.valor);
			if (data.action == 'Activar'){
				$(btn).removeClass('btn btn-danger');
				$(btn).addClass('btn btn-success');
			}else{
				$(btn).removeClass('btn btn-success');
				$(btn).addClass('btn btn-danger');
			}		
		}, 'json');

	});

	//Agregar Estudios al sistema
	$('#frmEstudio').on('submit', function(e){
		if ($(this).attr('data-id').toString().trim() ==''){
			e.preventDefault();

			var url = $(this).attr('action');

			$.post(url, $(this).serialize(), function(data){
				$('#add_estudio').append(data.response);
				$('#id_nombre').val('').focus();
				$('#id_lugar').val('');
				$('#id_periodo').val('');
			}, 'json');
		}
	});

	//eliminar los Estudios del sistema
	$('.btn-destudio').on('click', function(){
		var id = $(this).attr('data-id');
		var url = $(this).attr('data-url');
		var btn=$(this);
		$.get(url, {'id':id},function(data){
			$(btn).html(data.action);
			$('#d_estudio-'+ id).fadeOut();
			
		}, 'json');

	});

	//activar parroquias del sistema
	$('.btn-Aparroquia').on('click', function(){
		var id = $(this).attr('data-id');
		var url = $(this).attr('data-url');
		var btn=$(this);
		$.get(url, {'id':id},function(data){
			$(btn).html(data.action);
			$('#estado-' + id).text(data.valor);
			if (data.action == 'Activar'){
				$(btn).removeClass('btn btn-danger');
				$(btn).addClass('btn btn-success');
			}else{
				$(btn).removeClass('btn btn-success');
				$(btn).addClass('btn btn-danger');
			}		
		}, 'json');

	});

	//agregar Parroquias al sistema
	$('#frmParroquia').on('submit', function(e){
		if ($(this).attr('data-id').toString().trim() ==''){
			e.preventDefault();
			var url = $(this).attr('action');
			var data = new FormData($('#frmParroquia').get(0));

			$.ajax({
				url: url,
				type: $(this).attr('method'),
				data: data,
				cache: false,
				processData: false,
				contentType: false,
				success: function(data) {
				    $('#add_parroquia').append(data.response);
					$('#id_nombre').val('').focus();
					$('#id_descripcion').val('');
					$('#id_telefono').val('');
					$('#id_direccion').val('');
					$('#id_imagen').val('');
					$('#id_empleado').val('');
					$('#id_municipio').val('');
				}
			});
		}
		
	});





	
})