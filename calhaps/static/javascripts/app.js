function toggle_switch(label_for, element) {
	if($(element).is(":checked")){
		$("label[for="+label_for+"]").parent().css('background','white');
		$("label[for="+label_for+"]").parent().css('color','black');
	} else {
		$("label[for="+label_for+"]").parent().css('background','transparent');
		$("label[for="+label_for+"]").parent().css('color','white');
	}

	// refresh list based on filter
}