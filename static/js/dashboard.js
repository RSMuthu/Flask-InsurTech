// functionalities for the Dashboard.html

function get_cookie_value(name) { // not using as of now...
  // to get the cookie value from the page
  var result = document.cookie.match("(^|[^;]+)\\s*" + name + "\\s*=\\s*([^;]+)")
  return result ? result.pop() : ""
}

var form_dict = {}
$(document).ready(function () {
  // load the table with list of companies as soon as the page is loaded.
  load_table();
});

function load_table() {
  // loads the table with ajax call to server
  // Also this will generate a dataTable -- table with sort, pagination, search
  $.ajax({
      dataType  : 'json',
      method : 'GET',
      url : '/company/all',
      contentType: "application/json",
      success: function(response) {
        if (response.length == 0) {
          $("#content").html("<h1>No Entry Found");
        } else {
          form_dict={};
          create_table(response);
          $('#dtable').DataTable();
        }
      },
      error: function(response) {
        var x = JSON.parse(response.responseText);
        alert("Error: " + x.msg);
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
  head.setAttribute('class', 'thead-dark');
  table.appendChild(head);
  var htr = document.createElement('TR');
  head.appendChild(htr);
  var arr = ["Company Name", "Company Address", "Contact Name", "Contact Email", "Product", "Form info"]
  for (var i=0; i< arr.length; i++){
    th = document.createElement('TH')
    th.appendChild(document.createTextNode(arr[i]));
    htr.appendChild(th)
  }
  var body = document.createElement('TBODY');
  table.appendChild(body);
  for (var i=0; i<data.length; i++){
    var tr = document.createElement("TR");
    table_elem_create(data[i]["c_name"], tr);
    table_elem_create(data[i]["c_addr"], tr);
    table_elem_create(data[i]["contact_name"], tr);
    table_elem_create(data[i]["contact_email"], tr);
    table_elem_create(data[i]["product"], tr);
    if (data[i]['is_form_done']) {
      form_dict[i] = data[i]["form_data"];
      table_elem_create("<button data-toggle='modal' data-target='#form_modal' class='form-control btn btn-success' onclick='update_form_modal("+i+")'>show form data</button>", tr);
    } else {
      _id = i+1;
      table_elem_create("Form not submitted<br><button onclick='notifier("+ _id +")' class='form-control btn btn-primary'>notify contact</button>", tr);
    }
    body.appendChild(tr);
  }
  document.getElementById("content").appendChild(table);
}

function notifier(i) {
  // triggers ajax call to server requesting to send email to the company's contact person
  $.ajax({
    dataType  : 'json',
    method : 'GET',
    url : '/company/mail_to_contact/'+i,
    contentType: "application/json",
    success: function(response) {
      alert("Email has been sent.");
    },
    error: function(response) {
      var x = JSON.parse(response.responseText);
      alert(x.msg);
    }
  });

}

function update_form_modal(i) {
  // this helps to update the modal with the details of the form submitted by contact person
  var data = JSON.parse(form_dict[i]);
  document.getElementById("serv_name").innerHTML = data['serv_name'];
  document.getElementById("constituion").innerHTML = data['constituion'];
  document.getElementById("scope").innerHTML = data['scope'];
  document.getElementById("is_indian").innerHTML = data['is_indian'];
  document.getElementById("how_sp").innerHTML = data['how_sp'];
  document.getElementById("src_code").innerHTML = data['src_code'];
  document.getElementById("site").innerHTML = data['site'];
  document.getElementById("commercial").innerHTML = data['commercial'];
  document.getElementById("time").innerHTML = data['time'];
  document.getElementById("auto_renew").innerHTML = data['auto_renew'];
  document.getElementById("extra").innerHTML = data['extra']+"<br>"+data['other'];
}

function table_elem_create(content, row) {
    // single <td> creation utility
    td = document.createElement('TD');
    td.innerHTML = content;
    row.appendChild(td);
}

function create_company() {
  // makes ajax request to server to create a company with provided info
  var product = $("#product option:selected").val();
  if (product == '' || $('#c_name').val().trim() == '' || $('#c_addr').val().trim() == '' || $('#contact_name').val().trim() == '' || $('#contact_email').val().trim() == '') {
    alert("please enter all the fields...");
  } else {
    $.ajax({
      dataType  : 'json',
      data : JSON.stringify({
          c_name : $('#c_name').val().trim(),
          c_addr: $('#c_addr').val().trim(),
          contact_name: $('#contact_name').val(),
          product: product,
          contact_email: $('#contact_email').val().trim()
        }),
        method : 'POST',
        url : '/company',
        contentType: "application/json",
        success: function(response) {
          alert(response.msg);
          location.href="/dashboard";
        },
        error: function(response) {
          var x = JSON.parse(response.responseText);
          alert(x.msg);
        }
      });
    //console.log($('#c_name').val() +" "+ $('#c_addr').val() +" "+ $('#contact_name').val() +" "+ $('#contact_email').val() + " " + product)
    $('#inp').modal('hide');
  }
}

function logout() {
  // triggers logout request to the server
  $.ajax({
    dataType  : 'json',
      method : 'DELETE',
      url : '/auth/signout',
      contentType: "application/json",
      success: function(response) {
        alert("logged out...");
        location.href="/";
      },
      error: function(response) {
        var x = JSON.parse(response.responseText);
        alert("Error: " + x.msg);
      }
    });
}
