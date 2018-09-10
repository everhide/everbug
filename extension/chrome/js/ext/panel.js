var queries_count = 0;
var queries_time = 0;
var current_alias = '__all__';
var aliases = [current_alias];

function isJSON(val) {
    if (typeof val !== 'string')
        val = JSON.stringify(val);
    try {
        JSON.parse(val);
        return !0
    } catch (e) {
        return !1
    }
}

function init(handle) {
    handle.$('#tabs li').hide();
    handle.$('.tb_help').show().addClass('active');
    handle.$(".panel").hide();
    handle.$('#tab_help').show();
    handle.$("ul#tabs li").click(function() {
        handle.$("ul#tabs li").removeClass("active");
        $(this).addClass("active").removeClass('has_unread');
        handle.$(".panel").hide();
        var actTab = $(this).find("a").attr("href");
        handle.$(actTab).show();
        return !1
    });
    clear(handle)
}

function clear(handle) {
    handle.$('#tabs li').hide();
    handle.$('.tb_help').show();
    queries_count = 0;
    queries_time = 0;
    aliases = ['__all__'];
    handle.$('.context-view').empty();
    handle.$('#tab_queries .info').empty();
    handle.$('#db_filter').empty().append($("<option></option>").attr("value", '__all__').text('ALL'));
    handle.$('.queries').empty();
    handle.$('.profile-view').empty()
}

function filterQueries(handle, alias) {
    var rows = handle.$('.queries > table > tbody > tr');
    if (alias === '__all__') {
        rows.show()
    } else {
        rows.hide();
        handle.$('.queries .' + alias).show()
    }
}

function appendContext(handle, data) {
    handle.$('.tb_context').addClass('has_unread');
    var ul = handle.$('.context-view');
    $.each(data, function(index, obj) {
        var name = obj[0],
            value = obj[1],
            cls = obj[2],
            ext = obj[3],
            cnt = obj[4];
        var is_inline = !((ext === 1) || (ext === 2));
        var item = $('<li>').append($('<div>', {
            'class': 'item'
        }).append($('<span>', {
            'class': 'ext'
        }).append(cls)).append($('<span>', {
            'class': 'name'
        }).append(name + ' = ')).append($('<span>', {
            'class': 'value'
        })));
        if ((ext === 1) || (ext === 2)) {
            if (isJSON(value)) {
                value = JSON.stringify(value, null, '\t')
            }
        }
        item.find('.ext').addClass('ext_' + ext);
        if (is_inline !== !0) {
            item.find('.item').addClass('expandable').append($('<span>').addClass('expand').addClass('open'));
            item.append($('<div>', {
                'class': 'content'
            }).append($('<div>', {
                'class': 'inner'
            }).append(value)));
            item.find('.value').text('[ items: ' + cnt + ' ]')
        } else {
            item.find('.value').text(value)
        }
        if (cls === 'str') {
            if (value.length < 50) {
                item.find('.value').empty().text(value);
                item.find('.content').remove();
                item.find('.expand').remove();
                item.find('.item').removeClass('expandable')
            } else {
                item.find('.value').empty().text('[ length: ' + value.length + ' ]');
                item.find('.inner').addClass('wrap_text')
            }
        }
        if ((ext >= 1) && (ext <= 3) && (isJSON(value) === !0)) {
            item.find('.inner').addClass('json_code')
        }
        ul.append(item)
    });
    hljs.initHighlightingOnLoad();
    handle.$('.json_code').each(function(i, block) {
        hljs.highlightBlock(block)
    });
    handle.$(".context-view .content").hide();
    handle.$(".context-view .item").click(function() {
        var item = $(this).parent();
        if (item.hasClass('active')) {
            item.removeClass('active');
            item.find('.expand').removeClass('close').addClass('open');
            item.find('.content').hide()
        } else {
            item.addClass('active');
            item.find('.expand').removeClass('open').addClass('close');
            item.find('.content').show()
        }
        return !1
    })
}

function appendQueries(handle, data) {
    handle.$('.tb_queries').addClass('has_unread');
    if (handle.$('.queries').text().length === 0) {
        var create_table = $('<table>').append($('<thead>').append($('<tr>').append($('<td width="5%">').text('Time')).append($('<td width="45%">').text('Explain')).append($('<td width="50%">').text('Sql')))).append($('<tbody>'));
        handle.$('.queries').append(create_table)
    }
    var filter = handle.$('#db_filter');
    var table_body = handle.$('.queries table').find('tbody');
    $.each(data, function(alias, queries) {
        if (!aliases.includes(alias)) {
            aliases.push(alias);
            filter.append($("<option></option>").attr("value", alias).text(':: ' + alias))
        }
        $.each(queries, function(index, query) {
            queries_time += parseFloat(query.time);
            queries_count += 1;
            var explains = '';
            $.each(query.explain, function(index, expl) {
                explains = explains + expl + '\n'
            });
            table_body.append($('<tr>', {
                'class': alias
            }).append($('<td>').text(query.time)).append($('<td style="white-space: pre-wrap;">').text(explains)).append($('<td>', {
                'class': 'sql_code'
            }).text(query.sql)))
        })
    });
    hljs.initHighlightingOnLoad();
    var info = handle.$('#tab_queries .info');
    info.text('Total queries: ' + queries_count + ', total time: ' + queries_time + ' ms');
    handle.$(".queries > table > tbody  > tr").each(function() {
        var cell = $(this).find("td").eq(2);
        cell.text(sqlFormatter.format(cell.text(), {
            language: 'sql',
            indent: "\t"
        }))
    });
    if (!aliases.includes(current_alias)) {
        current_alias = '__all__'
    }
    filter.val(current_alias);
    filterQueries(handle, current_alias);
    filter.click(function() {
        var sel = $(this).find('option:selected').val();
        if (sel !== current_alias) {
            current_alias = sel
        }
        filterQueries(handle, current_alias);
        return !1
    });
    handle.$('.sql_code').each(function(i, block) {
        hljs.highlightBlock(block)
    })
}

function appendProfiles(handle, data) {
    handle.$('.tb_profile').addClass('has_unread');
    if (handle.$('.profile-view').find('ul').text().length === 0) {
        handle.$('.profile-view').append('<ul>')
    }
    var list = handle.$('.profile-view').find('ul');
    $.each(data, function(i, profile) {
        var li = $('<li>', {
            'class': 'profile'
        }).append($('<div>', {
            'class': 'name'
        }).append($('<span>', {
            'class': 'func'
        }).text('Method: ' + profile.method)).append($('<span>', {
            'class': 'module'
        }).text(profile.module)).append($('<div>').append($('<span>', {
            'class': 'totals'
        }).text('Total calls: ' + profile.total_calls + ', total time: ' + profile.total_time)).append($('<span>', {
            'class': 'expand close'
        })))).append($('<div>', {
            'class': 'content'
        }).hide().append($('<table>').append($('<thead>').append($('<tr>').append($('<td width="5%">').text('ncalls')).append($('<td width="5%">').text('tottime')).append($('<td width="5%">').text('cumtime')).append($('<td width="85%">').text('call')))).append($('<tbody>'))));
        var rows = li.find('tbody');
        $.each(profile.lines, function(i, line) {
            rows.append($('<tr>').append($('<td>').text(line[0])).append($('<td>').text(line[1])).append($('<td>').text(line[2])).append($('<td>').text(line[3])))
        });
        list.append(li)
    });
    handle.$(".profile-view .name").unbind('click');
    handle.$(".profile-view .name").click(function() {
        var item = $(this).parent();
        if (item.hasClass('active')) {
            item.removeClass('active');
            item.find('.expand').removeClass('close').addClass('open');
            item.find('.content').hide()
        } else {
            item.addClass('active');
            item.find('.expand').removeClass('open').addClass('close');
            item.find('.content').show()
        }
        return !1
    })
}

function append(handle, data) {
    if (data !== undefined && data !== null) {
        var trace = JSON.parse(data);
        if ('context' in trace) {
            appendContext(handle, trace.context);
            handle.$('.tb_context').show()
        }
        if ('queries' in trace) {
            appendQueries(handle, trace.queries);
            handle.$('.tb_queries').show()
        }
        if ('profiles' in trace) {
            appendProfiles(handle, trace.profiles);
            handle.$('.tb_profile').show()
        }
    }
    if (handle.$('#tabs > li:visible').length > 1) {
        if (handle.$("ul#tabs").find('li.active').text() === 'Help') {
            handle.$("ul#tabs").find('li:visible:first').click()
        }
    }
    handle.$("ul#tabs").find('li.active').removeClass('has_unread')
}