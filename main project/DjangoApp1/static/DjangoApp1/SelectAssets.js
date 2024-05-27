
var selectedButtonsIDs = selectedButtonsString.split(',')
for (i = 0; i < selectedButtonsIDs.length; i++) {
    selectedButtonsIDs[i] = "selectedassetid_" + selectedButtonsIDs[i].trim();
}

for (const buttonID of selectedButtonsIDs) {
    if (document.getElementById(buttonID) != null) { // element exists
        document.getElementById(buttonID).textContent = "Added! (Click to Deselect)";
    }
}


SelectButton = function (buttonID) {
    // check whether button is already selected
    var selected = false;
    var index = 0; // index of button if it is in the list
    for(const button of selectedButtonsIDs){
        if (button == buttonID) {
            selected = true;
            break;
        }
        index++;
    }
    if (selected) { // remove from selected buttons
        var index = selectedButtonsIDs.splice(index, 1);
        document.getElementById(buttonID).textContent = "Add to Selected Assets";
    }
    else { // add to selected buttons
        selectedButtonsIDs.push(buttonID);
        document.getElementById(buttonID).textContent = "Added! (Click to Deselect)";
    }
}

PostSelectedAssetData = function () {
    fetch('/selected_assets', {
        method: "POST",

        body: JSON.stringify({
            buttonIDs: String(selectedButtonsIDs),
            identifier: "UpdatingSelectedAssets"
        }),

        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrftoken
        }
    }).then(response => response.json()).then(json => console.log(json));
}


/*
foreach(button in document.getElementsByClassName("selectAssetButtons")){
    if (button.id in selectedButtonIDs) {
        button.textContent = "Selected! (click to deselect)";
    }
    else {
        button.textContent = "Select asset";
    }
}
*/


