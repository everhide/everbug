var hwd = null;
var port = null;
var tab = chrome.devtools.inspectedWindow.tabId;

chrome.devtools.panels.create("Everbug", "../img/icons/icon_32.png", "../html/panel.html", function (plugin){
    plugin.onShown.addListener(function captureHandle(handleWindow){
        hwd = handleWindow;
        port = chrome.runtime.connect({name: 'everbug-devtool'});
        port.postMessage({name: 'init', tab_id: tab});
        port.onMessage.addListener(messageDispatcher)
    })
});

function getTrace(url, trace_id){
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        data: {'trace': !0},
        beforeSend: function (xhr){
           xhr.setRequestHeader("Accept", "application/json, text/plain, */*");
           xhr.setRequestHeader("TRACE-ID", trace_id)
        },
        success: function (data){
           append(hwd, JSON.stringify(data))
        }
    })
}

function messageDispatcher(msg){
    if (msg.tab_id === tab){
        switch (msg.status){
        case 'initiated':
            init(hwd);
            break;
        case 'clear':
            clear(hwd);
            break;
        case 'loading':
            break;
        case 'complete':
            break;
        case 'trace':
            append(hwd, getTrace(msg.url, msg.trace_id));
            break
        }
    }
}
