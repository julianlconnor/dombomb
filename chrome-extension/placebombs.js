document.body.style['cursor'] = 'crosshair';

/*
* Set bomb on click, send to server. Change this from onclick to something else.
*/
disableLinks();
document.onclick = createBomb;
function createBomb(e) {
    e.preventDefault();
    var coords = findClickPos(e),
        xhr = new XMLHttpRequest(),
        postString = "x="+ coords.x + "&y="+ coords.y + "&identifier=" + encodeURIComponent(window.location);
    xhr.open("POST", "http://184.72.230.86/?" + postString, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        console.log(xhr.responseText);
      }
    };
    console.log('[setBomb] ', postString);
    xhr.send("x="+ coords.x + "&y="+ coords.y + "&identifier=" + window.location);
    document.onclick = null;
    document.body.style['cursor'] = 'auto';
    enableLinks();
}

function disableLinks() {
    var links = document.getElementsByTagName('a');

    for ( var i = 0; i < links.length; i++ ) {
        links[i].style['cursor'] = 'crosshair';
    }
}
function enableLinks() {
    var links = document.getElementsByTagName('a');

    for ( var i = 0; i < links.length; i++ ) {
        links[i].style['cursor'] = 'pointer';
    }
}
