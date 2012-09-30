chrome.browserAction.onClicked.addListener(function(tab) {
    /*
    * Flow for placing a bomb.
    *
    * 1. Cursor, allow person to click.
    * 2. After click make api call with coords and url.
    * 3. Stop execution.
    *
    */
    chrome.tabs.executeScript(null, {file: "placebombs.js"});
});
