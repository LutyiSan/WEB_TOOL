
let protocol = document.querySelector('#start-form select');
let protocol_submit = document.querySelector('#protocol-submit');
let bacnet = document.querySelector('#bacnet-form select');
let bacnet_submit = document.querySelector('#bacnet-submit')

protocol_submit.addEventListener("click", function(){
    console.log(protocol.value)
    if (protocol.value == 'bacnet') {
   document.querySelector('#bacnet-form').style.display = "block";
   document.querySelector('#modbus-read').style.display = "none";
    } else {
   document.querySelector('#modbus-read').style.display = "block";
   document.querySelector('#bacnet-form').style.display = "none";

    }
    }
)
bacnet_submit.addEventListener("click", function(){

    if (bacnet.value == 'object-list') {
   document.querySelector('#bacnet-object-list').style.display = "block";
   document.querySelector('#bacnet-read').style.display = "none";
   document.querySelector('#bacnet-form #bacnet-submit').type = 'button';
    } else if (bacnet.value == 'read-property'){
   document.querySelector('#bacnet-read').style.display = "block";
   document.querySelector('#bacnet-object-list').style.display = "none";
   document.querySelector('#bacnet-form #bacnet-submit').type = 'button';

    }else{
    document.querySelector('#bacnet-read').style.display = "none";
    document.querySelector('#bacnet-object-list').style.display = "none";
    document.querySelector('#bacnet-form #bacnet-submit').type = 'submit';

    }
    }
)














