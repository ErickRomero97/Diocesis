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
})