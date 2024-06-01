Dropzone.options.fileDropzone = {
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 16, // MB
    acceptedFiles: ".jpeg,.jpg,.png,.gif,.pdf,.doc,.docx,.xls,.xlsx,.txt,.zip",
    init: function () {
        this.on("success", function (file, response) {
            alert("File uploaded successfully!");
        });
        this.on("error", function (file, response) {
            alert("An error occurred while uploading the file.");
        });
    }
};
