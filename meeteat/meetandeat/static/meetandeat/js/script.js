$pageBody = document.querySelector("body");
$pageID = $pageBody.id;
if($pageID == "create-event" || $pageID == "edit-event") {
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


