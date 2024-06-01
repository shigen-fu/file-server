document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.share-btn').forEach(function (button) {
        let qrcodeElement = button.closest('.file-actions').querySelector('.file-qrcode');
        let fileUrl = qrcodeElement.getAttribute('data-url');
        new QRCode(qrcodeElement, {
            text: fileUrl,
            width: 64,
            height: 64,
        });

        button.addEventListener('click', function () {
            // Hide all other QR codes
            document.querySelectorAll('.file-qrcode').forEach(function (element) {
                element.style.display = 'none';
            });

            // Toggle the current QR code
            if (qrcodeElement.style.display === 'none' || qrcodeElement.style.display === '') {
                qrcodeElement.style.display = 'block';
            } else {
                qrcodeElement.style.display = 'none';
            }
        });
    });

    // Hide QR code when clicking outside
    document.addEventListener('click', function (event) {
        if (!event.target.matches('.share-btn')) {
            document.querySelectorAll('.file-qrcode').forEach(function (element) {
                element.style.display = 'none';
            });
        }
    });
});
