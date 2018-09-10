var connections = {};

function isTraced(headers) {
    for (var i = 0; i < headers.length; ++i) {
        if (headers[i].name === 'HTTP_HAS_TRACE') {
            return headers[i].value
        }
    }
    return 0
}

browser.runtime.onConnect.addListener(function(port){
    var extensionListener = function(message, sender, sendResponse){
        if (message.name === "init"){
            connections[message.tab_id] = port;
            connections[message.tab_id].postMessage({
                'status': 'initiated',
                'tab_id': message.tab_id
            });
            return null
        }
    };
    port.onMessage.addListener(extensionListener);
    port.onDisconnect.addListener(function(port){
        port.onMessage.removeListener(extensionListener);
        var tabs = Object.keys(connections);
        for (var i = 0, len = tabs.length; i < len; i++){
            if (connections[tabs[i]] === port){
                delete connections[tabs[i]];
                break
            }
        }
    })
});

browser.webRequest.onHeadersReceived.addListener(function callback(details) {
    if (details.tabId in connections) {
        if ((details.frameId >= 0) && ((details.type === 'main_frame') || (details.type === 'xmlhttprequest'))) {
            if (details.type === 'main_frame') {
                connections[details.tabId].postMessage({
                    status: 'clear',
                    tab_id: details.tabId
                })
            }
            var trace_id = isTraced(details.responseHeaders);
            if (trace_id >= 1 && trace_id !== 'undefined'){
                connections[details.tabId].postMessage({
                    'status': 'trace',
                    'tab_id': details.tabId,
                    'trace_id': trace_id,
                    'url': details.url
                })
            }
        }
    }
},
{
    urls: ['<all_urls>'],
    types: ['main_frame', 'xmlhttprequest']
}, ['responseHeaders']);

browser.webRequest.onBeforeSendHeaders.addListener(function(details){
    if (details.frameId >= 0){
        if (!('TRACE-ID' in details.requestHeaders)){
            details.requestHeaders.push({
                name: 'REQUEST-ID',
                value: details.requestId
            })
        }
    }
    return {requestHeaders: details.requestHeaders}
}, { urls: ["<all_urls>"]}, ["blocking", "requestHeaders"]);

browser.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (tabId in connections){
        switch (changeInfo.status){
            case 'complete':
                connections[tabId].postMessage({
                    'status': 'complete',
                    'tab_id': tabId
                });
                break;
            case 'loading':
                connections[tabId].postMessage({
                    'status': 'loading',
                    'tab_id': tabId
                });
                break
        }
    }
})
