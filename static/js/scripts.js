
//profile pic function
$(document).ready(function(){
    var icon_label = $('#profile-icon-label')
    var profile_pic_input = $('#profile-pic-upload')

    profile_pic_input.change(function(){
            if (this.files[0].size > 5242880) {
                icon_label.toggleClass('text-danger')
                icon_label.text('File must be less than 5mb')
                this.value = ""
            }
            else{
                icon_label.text(this.files[0].name)
            }
        }
        
    )}
)