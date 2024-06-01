document.addEventListener('DOMContentLoaded', function () {
    let qrcodeElement = document.getElementById('qrcode');
    if (qrcodeElement) {
        new QRCode(qrcodeElement, {
            text: window.location.href,
            width: 128,
            height: 128,
        });
    }

    let shareButton = document.querySelector('.share-btn');
    shareButton.addEventListener('mouseenter', function () {
        qrcodeElement.style.display = 'block';
    });

    shareButton.addEventListener('mouseleave', function () {
        qrcodeElement.style.display = 'none';
    });

    document.querySelectorAll('.file-qrcode').forEach(function (element) {
        let fileUrl = element.getAttribute('data-url');
        new QRCode(element, {
            text: fileUrl,
            width: 64,
            height: 64,
        });
    });
});
