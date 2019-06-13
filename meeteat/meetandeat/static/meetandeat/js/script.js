$pageBody = document.querySelector("body");
$pageID = $pageBody.id;
if($pageID === "create-event" || $pageID === "edit-event") {
    $datePicker = $pageBody.querySelector("#datetime");
    if(!$datePicker.value) {
        // $dateString = new Date.toLocaleString();
        $datePicker.value = getLocalDateTime();
    }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

if($pageID === "profile") {
    function create_post() {
    console.log("create post is working!");
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
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
    };
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


