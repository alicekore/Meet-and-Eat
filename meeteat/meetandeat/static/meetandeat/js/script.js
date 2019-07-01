$pageBody = document.querySelector("body");
$pageID = $pageBody.id;

//##### Event Form javascript #####
if($pageID === "create-event" || $pageID === "edit-event") {
    $datePicker = $pageBody.querySelector("#datetime");
    if(!$datePicker.value) {
        // $dateString = new Date.toLocaleString();
        $datePicker.value = getLocalDateTime();
    }
}

function zeroPadded(val) {
  if (val >= 10)
    return val;
  else
    return '0' + val;
}

function getLocalDateTime() {
    d = new Date();
  return d.getFullYear()
      +"-"
      +zeroPadded(d.getMonth() + 1)
      +"-"
      +zeroPadded(d.getDate())
      +"T"
      +zeroPadded(d.getHours())
      +":"
      +zeroPadded(d.getMinutes());
}
//###################


//##### Profile javascript #####
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

if($pageID === "profile") {

    if (window.innerWidth < 800 || window.innerHeight < 600 || detectmob()) {
        $('#deleteModal').on('show.bs.modal', function (e) {
            e.preventDefault();
            document.location = $('#deleteAccountButton').attr('href');
        })

    }

    $('#profilePictureUpdate').on('change',function(){
                //get the file name
                let fileName = $(this).val().replace('C:\\fakepath\\', " ");
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            });


    function create_post() {
    console.log("create post is working!");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url : $('#deleteAccountForm').attr("action"), // the endpoint
        type : "POST", // http method
        data : { password : $('#deleteAccountPassword').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#deleteAccountPassword').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            // let receivedData = JSON.parse(json);
            if(json.status === 0) {
                console.log(json.url);
                document.location = json.url;
                if(!document.getElementById('deleteAccountInvalidFeedback').classList.contains('invisible')) {
                    document.getElementById('deleteAccountInvalidFeedback').classList.add("invisible");
                }
                if(document.getElementById("deleteAccountPassword").classList.contains("is-invalid")) {
                    document.getElementById("deleteAccountPassword").classList.remove("is-invalid");
                    document.getElementById("deleteAccountPassword").classList.add("is-valid");
                }

            }
            if(json.status === 1) {
                if(document.getElementById('deleteAccountInvalidFeedback').classList.contains('invisible')) {
                    document.getElementById('deleteAccountInvalidFeedback').classList.remove("invisible");
                    document.getElementById('deleteAccountInvalidFeedback').innerText = json.message;

                }
                if(!document.getElementById("deleteAccountPassword").classList.contains("is-invalid")) {
                    document.getElementById("deleteAccountPassword").classList.add("is-invalid");
                }
            }
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    }
}
//################


//##### Register javascript #####
if($pageID === "register") {
    $('#profilePicture').on('change',function(){
                //get the file name
                let fileName = $(this).val().replace('C:\\fakepath\\', " ");
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            });
}
//################

function detectmob() {
 if( navigator.userAgent.match(/Android/i)
 || navigator.userAgent.match(/webOS/i)
 || navigator.userAgent.match(/iPhone/i)
 || navigator.userAgent.match(/iPad/i)
 || navigator.userAgent.match(/iPod/i)
 || navigator.userAgent.match(/BlackBerry/i)
 || navigator.userAgent.match(/Windows Phone/i)
 ){
    return true;
  }
 else {
    return false;
  }
}


