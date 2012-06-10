$(document).ready(function(){
    request_next_page(bind_scroll)
    $('#tag-button').colorbox({inline: 'true', width: '50%', href: '#tagdialog'});
    $('#taginput').typeahead({ source: tag_list, items: 5, });
    $('#tagform').submit(function() {
        var val = $('#taginput').val();
        if (val.length == 0)
            return false;
        var tag = $('<div/>');
        tag.attr('class', 'taglive');
        tag.text(val);
        $('#taglivebar').append(tag);
        $('#taginput').val('');
        return false;
    });
})
var last = "";

function bind_scroll() {
    $(window).bind('scroll', function() {
        if ($(window).scrollTop() == $(document).height() - $(window).height()) { 
            $(window).unbind('scroll')
            request_next_page(bind_scroll)
        }
    }) 
}

function request_next_page(callback) {
    $.ajax({
        type: "GET",
        url: callback_url + '?from=' + last,
        timeout: 15000,
        success: function(d) {
            last = d[d.length-1].creation;
            var pack = $("<ul class='imagepack'></ul>")
            for(var i=0; i<d.length; i++) {
                var p = d[i]
                var buf = []
                var cc = p.tags.length > 0 ? 'thumb tagged' : 'thumb'
                buf.push("<li class='" + cc + "' thumb_id='" + p.id + "' tags='" + p.tags + "'>")
                var s = p.width > p.height ? "wi" : "hi";
                var factor = Math.min(200 / p.width, 200 / p.height)
                var w = p.width * factor
                var h = p.height * factor
                var path_tokens = p.thumbnail.split('/')
                var path = path_tokens[path_tokens.length-1]
                buf.push("<img class='image' src='/cassad/thumbnails/" + path + "' style='width:" + w + "px;height:" + h +"px' />")
                buf.push("<div class='overlay overlay-top'></div>")
                buf.push("<div class='overlay overlay-bottom'>")
                buf.push(p.width + "x" + p.height)
                buf.push("</div>")
                buf.push("</li>")
                
                var elem_html = buf.join('')
                pack.append(elem_html)
            }
            var brick = $("<div class='brick'><a href='" + window.location + last + "'>Page</a></div>")
            pack.append(brick)

            if ($('.imagepack').length == 0)
                $('#page').append(pack)
            else
                $(".imagepack:last").after(pack)
            if (last != '')
                callback()
        }
    });
}

$(".image").live('click', function(){
    var thumb = $(this).parent('.thumb')
    thumb.toggleClass('selected')
});

$(".thumb").live('mouseenter', function(){ $(this).find(".overlay").toggle(); });
$(".thumb").live('mouseleave', function(){ $(this).find(".overlay").toggle(); });

$("#tag-button").live('click', function() {

    var tags = []
    $('.selected').each(function(index, elem) {
        var elem_tags = $(elem).attr('tags').split(',')
        for (var i=0; i<elem_tags.length; i++) {
            var t = elem_tags[i]
            if ((tags.indexOf(t) == -1)&&(t.length > 0))
                tags.push(t)
        }
    });
    var taglivebar = $('#taglivebar');
    taglivebar.children().remove();
    for (var i=0; i<tags.length; i++) {
        var tagelem = $('<div />');
        tagelem.attr('class', 'taglive');
        tagelem.text(tags[i]);
        taglivebar.append(tagelem);
    }
    $('#taginput').focus();
})

$('#tagcancel').live('click', function() {
    $.colorbox.close();
})
$('#tagsave').live('click', function() {
    $.colorbox.close();

    var tags = [];
    $('#taglivebar').children().each(function(idx, elem) {
        tags.push($(elem).text());
    });
    var tags_str = tags.join(', ');
    var selected = []
    $('.selected').each(function(index, elem) {
        selected.push($(elem).attr("thumb_id"))
        $(elem).attr('tags', tags_str)
    })
    $.ajax({
        type: "POST",
        data: JSON.stringify({ selected: selected, tags: tags }),
        url: "/cassad/api/tags-bulk/",
	processData: false,
        timeout: 15000,
        success: function(d) {
            $('.selected').removeClass('selected')
        }
    })
})

$('#del-button').live('click', function() {
    var selected = []
    $('.selected').each(function(index, elem) {
        selected.push($(elem).attr("thumb_id"))
    })
    if (selected.length == 0)
        return false;
    if (!confirm('Are you sure you want to delete selected items?'))
        return false;
    $.ajax({
        type: "POST",
        data: JSON.stringify({ selected: selected, tags: ["deleted"] }),
	processData: false,
        url: "/cassad/api/tags-bulk/",
        timeout: 15000,
        success: function(d) {
            $('.selected').remove()
        }
    })
})

$('#clean-button').live('click', function() {
    $('.imagepack:not(:last)').remove()
})

$(function() {
    $('.tag').click(function() {
        var val = $(this).text();
        var tag = $('<div/>');
        tag.attr('class', 'taglive');
        tag.text(val);
        $('#taglivebar').append(tag);

    });
});

$('.overlay-top').live('click', function(){
    var id = $(this).parents('.thumb').attr('thumb_id');
    window.open('/cassad/image/' + id, '_blank');
});

$('.taglive').live('click', function(){
    var pthis = $(this);
    pthis.remove();
});

