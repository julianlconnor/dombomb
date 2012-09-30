function placeBomb() {
    chrome.tabs.getSelected(null, function(tab){
        tab.executeScript(null,
                           {code:"document.body.bgColor='red'"});
    });
}

placeBomb();

