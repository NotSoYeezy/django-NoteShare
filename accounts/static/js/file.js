function processSelectedFiles(fileInput) {
  let files = fileInput.files;
  fileInput.style.content = ''
  for (let i = 0; i < files.length; i++) {
    alert("Filename " + files[i].name);
    fileInput.style.content = files[i].name
  }
}