function updateUploadFileList() {
    var input = document.getElementById('files');
    var output = document.getElementById('fileList');
    output.innerHTML = "";

    var list = document.createElement("ol");
    for (var i = 0; i < input.files.length; ++i) {
        var list_entry = document.createElement("li");
        list_entry.textContent = input.files.item(i).name;
        list.appendChild(list_entry);
    }
    output.appendChild(list);
}

function initUpdateList() {
    updateUploadFileList();

    var uploadButton = document.getElementById("files");
    if (files) {
        files.addEventListener("change", updateUploadFileList);
    }
    else {
        console.warn("Could not find file upload button!");
    }
}

// initially update the list (so that cached files will be shown as well)
document.addEventListener("DOMContentLoaded", initUpdateList);
