$(document).on('ready', function() {
	$('.email-group').each(function(){
		extraEmails = $('.email-group').find('input').val();
		extraEmails = extraEmails.split(',');

		// leave first email and remove from array
		$('.email-group').find('input').val(extraEmails.shift());

		// > 1 as array has empty cell
		if (extraEmails.length > 1) {
			for (var i = extraEmails.length - 1; i >= 0; i--) {
				extraEmail = extraEmails[i];
				$(this).clone().insertAfter($(this))
					.find('input')
						.attr('placeholder', 'Papildus e-pasts')
						.attr('name', 'extra_emails[]')
						.prop('required', false)
						.val(extraEmail);
			}
		}
	});

	$('.add-extra-email').on('click', function(e){
		e.preventDefault();

		$(this).parent().prev().clone().insertBefore($(this).parent())
			.find('input')
				.attr('placeholder', 'Papildus e-pasts')
				.attr('name', 'extra_emails[]')
				.prop('required', false)
				.val('');
	});

	$("#input-4").fileinput({showCaption: false});

	$(".form_date").datetimepicker({
		format: "yyyy-mm-dd",
		language:  'lv',
		startView: 4,
		fontAwesome: 1,
		minView: 2,
		forceParse: 0,
		autoclose: true
	});

	$('.search_selectpicker').selectpicker({
		size: 8,
		liveSearch: true
	});

	var subspeciality = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		prefetch: {
			url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"subspeciality"}]}',
			cache : false,
			filter: function(list) {
			  return $.map(list.objects, function(classifier) {
					return { name: classifier.tag_lv, id: classifier.id };
			  });
			}
		}
	});
	subspeciality.initialize();

	function subspeciality_def(q, sync) {
		if (q === '') {
			sync(subspeciality.all()); // This is the only change needed to get 'ALL' items as the defaults
		} else {
			subspeciality.search(q, sync);
		}
	}

	$('#subspeciality').tagsinput({
		freeInput: true,
		trimValue: true,
		typeaheadjs: [
		{
			hint: true,
			highlight: true,
			minLength: 0
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			limit: 20,
			source: subspeciality_def
		}]
	});

	var danceskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"danceskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv };
		  });
		}
	  }
	});
	danceskill.initialize();

	$('#danceskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			name: 'danceskill_pool',
			displayKey: 'name',
			valueKey: 'name',
			source: danceskill.ttAdapter(),
			templates: {
				empty: '<div class="empty-message">Nekas nav atrasts</div>'
			}
		}]
	});

	var singskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"singskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	singskill.initialize();

	$('#singskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: singskill.ttAdapter(),
			templates: {
				empty: '<div class="empty-message">Nekas nav atrasts</div>'
			}
		}]
	});

	var musicskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"musicskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	musicskill.initialize();

	$('#musicskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: musicskill.ttAdapter()
		}]
	});

	var sportskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"sportskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	sportskill.initialize();

	$('#sportskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: sportskill.ttAdapter()
		}]
	});

	var swimskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"swimskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	swimskill.initialize();

	$('#swimskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  maxTags: 1,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: swimskill.ttAdapter()
		}]
	});

	var driveskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"driveskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	driveskill.initialize();

	$('#driveskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  maxTags: 1,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: driveskill.ttAdapter()
		}]
	});

	var languageskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"languageskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	languageskill.initialize();

	$('#languageskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: languageskill.ttAdapter()
		}]
	});

	var otherskill = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"otherskill"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
				return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	otherskill.initialize();

	$('#otherskill').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: otherskill.ttAdapter()
		}]
	});

	var want_participate = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		prefetch: {
			url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"want_participate"}]}',
			cache : false,
			filter: function(list) {
			  return $.map(list.objects, function(classifier) {
					return { name: classifier.tag_lv, id: classifier.id };
			  });
			}
		}
	});
	want_participate.initialize();

	$('#want_participate').tagsinput({
		freeInput: true,
		trimValue: true,
		typeaheadjs: [
		{
			hint: true,
			highlight: true,
			minLength: 0
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: want_participate.ttAdapter()
		}]
	});

	var dont_want_participate = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		prefetch: {
			url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"dont_want_participate"}]}',
			cache : false,
			filter: function(list) {
			  return $.map(list.objects, function(classifier) {
					return { name: classifier.tag_lv, id: classifier.id };
			  });
			}
		}
	});
	dont_want_participate.initialize();

	function dont_want_participate_def(q, sync) {
		if (q === '') {
			sync(dont_want_participate.all()); // This is the only change needed to get 'ALL' items as the defaults
		} else {
			dont_want_participate.search(q, sync);
		}
	}

	$('#dont_want_participate').tagsinput({
		freeInput: true,
		trimValue: true,
		typeaheadjs: [
		{
			hint: true,
			highlight: true,
			minLength: 0
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			limit: 20,
			source: dont_want_participate_def
		}]
	});

	var interested_in = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		prefetch: {
			url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"interested_in"}]}',
			cache : false,
			filter: function(list) {
			  return $.map(list.objects, function(classifier) {
					return { name: classifier.tag_lv, id: classifier.id };
			  });
			}
		}
	});
	interested_in.initialize();

	function interested_in_def(q, sync) {
		if (q === '') {
			sync(interested_in.all()); // This is the only change needed to get 'ALL' items as the defaults
		} else {
			interested_in.search(q, sync);
		}
	}

	$('#interested_in').tagsinput({
		freeInput: false,
		trimValue: true,
		typeaheadjs: [
		{
			hint: true,
			highlight: true,
			minLength: 0
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			limit: 20,
			source: interested_in_def
		}]
	});

	var tattoo = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"tattoo"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	tattoo.initialize();

	$('#tattoo').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: tattoo.ttAdapter()
		}]
	});

	var piercing = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"piercing"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	piercing.initialize();

	$('#piercing').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: piercing.ttAdapter()
		}]
	});

	var afraidof = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"afraidof"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	afraidof.initialize();

	$('#afraidof').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: afraidof.ttAdapter()
		}]
	});

	var religion = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"religion"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	religion.initialize();

	$('#religion').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: religion.ttAdapter()
		}]
	});

	var educational_institution = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"educational_institution"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	educational_institution.initialize();

	$('#educational_institution').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: educational_institution.ttAdapter()
		}]
	});

	var learned_profession = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"learned_profession"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	learned_profession.initialize();

	$('#learned_profession').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: learned_profession.ttAdapter()
		}]
	});

	var degree = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"degree"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	degree.initialize();

	$('#degree').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: degree.ttAdapter()
		}]
	});

	var workplaces = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"workplaces"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
		}
	});
	workplaces.initialize();

	$('#workplaces').tagsinput({
		freeInput: true,
		trimValue: true,
		typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: workplaces.ttAdapter()
		}]
	});

	var cb_tags = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"cb_tags"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	cb_tags.initialize();

	$('#cb_tags').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: cb_tags.ttAdapter()
		}]
	});

	var family_notes = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  prefetch: {
		url: '/api/classifier?q={"filters":[{"name":"category","op":"eq","val":"family_notes"}]}',
		cache : false,
		filter: function(list) {
		  return $.map(list.objects, function(classifier) {
			return { name: classifier.tag_lv, id: classifier.id };
		  });
		}
	  }
	});
	family_notes.initialize();

	$('#family_notes').tagsinput({
	  freeInput: true,
	  trimValue: true,
	  typeaheadjs: [
		{
			hint: true,
			highlight: true
		},
		{
			limit: 10,
			name: 'objects',
			displayKey: 'name',
			valueKey: 'name',
			source: family_notes.ttAdapter()
		}]
	});

	$('.bootstrap-tagsinput:has(.tag)')
		.append('<span class="tag label label-danger" title="Noņemt visas brikas"><span data-role="remove"></span></span>');

	$('.bootstrap-tagsinput .tag.label-danger').on('click', function(e){
		e.preventDefault();

		$(this).parent().next()
			.tagsinput('removeAll');
	});
});