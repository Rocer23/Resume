const uploadPictureBtn = document.querySelector('.photo-upload');

uploadPictureBtn.addEventListener('change', function() {
    displayPicture(this);
});

function displayPicture(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById('the-picture').setAttribute('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
        uploadPictureBtn.ariaHidden();
    }
}