// Function utilities for the Message Board page

$(document).ready(function () {
  // as soon the page is ready, the conversation table is getting loaded...
  load_table();
  $("#auto").click();
  $("#tsearch").on("keyup", function() { // for conversation search filter
    var value = $(this).val().toLowerCase();
    $("#dtbody tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$("#auto").click(function () { // add event handler for the Button to endable/disable the auto refresh of conversation table.
  var $this = $(this);
  if ($this.hasClass("btn-success")) {
    my_timer = setInterval(load_table, 5000); // refresh rate is 1 refresh per 5 sec
    $this.removeClass("btn-success").addClass("btn-danger");
    $this.html("Disable Auto Refresh");
  } else {
    clearInterval(my_timer);
    $this.removeClass("btn-danger").addClass("btn-success");
    $this.html("Enable Auto Refresh");
  }
});

function load_table() {
  // loads the conversation table through ajax call to server
  $.ajax({
      dataType  : 'json',
      method : 'GET',
      url : '/company/msg/' + $("#cid").val(),
      contentType: "application/json",
      success: function(response) {
        if (response.length == 0) { // handler when no msg in the conversation
          $("#tsearch").hide();
          $("#msg_content").html("<div style='text-align: center;vertical-align: middle;'><h1>No Message Found</h1></div>");
        } else {
          $("#tsearch").show();
          create_table(response); // table creation only if there are some messages
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
}

function create_table(data) {
  // build the table and its elemesnts DOM with the data input
  var table = document.createElement('table');
  table.setAttribute('id', 'dtable');
  table.setAttribute('class', 'table table-hover table-bordered table-sm');
  table.setAttribute('width', '100%');
  table.setAttribute('cellspacing', 0);
  var head = document.createElement('THEAD');
  //head.setAttribute('class', 'thead-dark');
  table.appendChild(head);
  var htr = document.createElement('TR');
  head.appendChild(htr);
  var arr = ["Sender", "Message"]
  for (var i=0; i< arr.length; i++){
    th = document.createElement('TH')
    th.appendChild(document.createTextNode(arr[i]));
    htr.appendChild(th)
  }
  var body = document.createElement('TBODY');
  body.setAttribute('id', 'dtbody');
  table.appendChild(body);
  for (var i=0; i<data.length; i++){
    var tr = document.createElement("TR");
    table_elem_create(data[i]["by"] + '<br>' +data[i]["tstamp"], tr, 25);
    table_elem_create(data[i]["msg"], tr, 75);
    body.appendChild(tr);
  }
  var div = document.getElementById("msg_content");
  while( div.childNodes[0] ) {
    div.removeChild( div.childNodes[0] );
  }
  div.appendChild(table);
}

function table_elem_create(content, row, width) {
  // single <td> creation
  td = document.createElement('TD');
  td.setAttribute('style', 'width:'+width+'%');
  td.innerHTML = content;
  row.appendChild(td)
}

function send_msg() {
  // adding message to the conversation
  if ($("#name").val().trim() == '' || $("#msg").val().trim() == ''){
    alert ("Please enter all the fields");
  } else {
    $.ajax({
      dataType  : 'json',
      data : JSON.stringify({
          name : $('#name').val().trim(),
          msg : $('#msg').val().trim()
        }),
        method : 'POST',
        url : '/company/msg/'+ $('#cid').val(),
        contentType: "application/json",
        success: function(response) {
          load_table();
        },
        error: function(error) {
          alert(error);
          console.log(error);
        }
      });
  }

}
