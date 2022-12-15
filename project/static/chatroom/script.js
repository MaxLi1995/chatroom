document.addEventListener('DOMContentLoaded', function () {
  if (document.URL.match('/room/[0-9]+$')) {
    if (homeIntervalRefNum != 0) {
      clearInterval(homeIntervalRefNum)
    }
    let id = document.URL.match(/[0-9]+$/);
    initial_load(id);
  } else {
    if (roomIntervalRefNum != 0) {
      clearInterval(roomIntervalRefNum)
    }
    if (document.getElementById('not_logged_in') == null) {
      homeIntervalRefNum = setInterval(function () {
        get_open_rooms();
      }, 1000);
      get_open_rooms();
    }
  }

})

function toggle() {
  document.getElementsByClassName('navbar-links')[0].classList.toggle('active');
}

roomIntervalRefNum = 0
homeIntervalRefNum = 0

function get_open_rooms() {
  fetch('/open_rooms')
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        text = "<h3 style='text-align: center; margin-top:48px;'>List of Open Rooms</h3>"
        for (room of result['rooms']) {
          text += `<div class="rooms"><div>${room['name']}</div>
          <div>Room onwer: ${room['creator']}</div>
          <button class="joinBTN" onclick='join_open_room("${room["name"]}")'>Join</button>
          </div>`
        }
        if (result['rooms'].length == 0) {
          text += `<div>No open rooms at the moment</div>`
        }
        document.getElementById("open_rooms").innerHTML = text
      }
    });
}

function show_error(error, reload = true) {
  if (roomIntervalRefNum != 0 && reload) {
    clearInterval(roomIntervalRefNum)
  }
  if (homeIntervalRefNum != 0 && reload) {
    clearInterval(homeIntervalRefNum)
  }
  if (document.getElementById("room") != null) {
    document.getElementById("room").style.display = "none";
  }
  errorText = `<div style='text-align: center;'>${error}</div>`;
  if (document.URL.match('/room/[0-9]+$')) {
    errorText += `<button class='btn btn-primary' style='display:block;margin-right: auto;margin-left: auto;' onclick="location.href='/';">Back to main page</button>`
  }
  document.getElementById("error").innerHTML = errorText
}

function load_room(id, scroll = false) {
  fetch('/room_info/' + id)
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        text = `<div id='names'><b>Users:</b><div style='padding: 4px 8px;'>${result['creator']}(owner)</div>`
        for (user of result['users']) {
          text += `<div style='padding: 4px 8px;'>${user}`
          if (result['my_room']) {
            text += `<button class='kickbtn' onclick='kick_user(${id}, "${user}")'>Kick</button>`
          }
          text += `</div>`
        }
        document.getElementById("room_members").innerHTML = text
        text = ``
        for (message of result['messages']) {
          text += `<div class='message'>` + message['user'] + `(` + message['timestamp'] + `):` + message['message'] + `</div>`
        }
        document.getElementById("room_page").innerHTML = text
        if (scroll) {
          var messagePage = document.getElementById("room_page");
          messagePage.scrollTop = messagePage.scrollHeight;
        }
      } else {
        show_error(result['error']);
      }
    });
}

function initial_load(id) {
  fetch('/room_info/' + id)
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        text = `<form id="new_message">
          <textarea class="form-control" id="message_body" style="padding:10px;resize:none;" placeholder="message"></textarea>`
        text += `<div class='exBTN'>
        <button type="button" class="btn btn-primary" style="margin:5px;" value="Submit" onClick="send_message(${id})">Submit</button>
        <div class='ex2BTN'>`
        if (result['my_room']) {
          text += `<button type="button" class="btn btn-primary" style="margin:5px;" value="Submit" onClick="delete_room(${id})">Delete Room</button>`
        }
        text += `<button type="button" class="btn btn-primary" style="margin:5px;" value="Submit" onClick="leave_room(${id})">Leave Room</button></div></div></form>`
        document.getElementById("room_control").innerHTML = text
        roomIntervalRefNum = setInterval(function () {
          load_room(id)
        }, 1000);
        load_room(id, true)
      } else {
        show_error(result['error']);
      }
    });
}

function kick_user(id, name) {
  fetch('/kick_user', {
    method: 'DELETE',
    body: JSON.stringify({
      roomId: id,
      username: name
    })
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        load_room(id)
      } else {
        show_error(result['error']);
      }
    });
}

function delete_room(id) {
  fetch('/delete/' + id, {
    method: 'DELETE'
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        window.location.href = "/";
      } else {
        show_error(result['error']);
      }
    });
}

function leave_room(id) {
  fetch('/leave_room/' + id, {
    method: 'DELETE'
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        window.location.href = "/";
      } else {
        show_error(result['error']);
      }
    });
}

function send_message(id) {
  fetch('/message', {
    method: 'POST',
    body: JSON.stringify({
      roomId: id,
      message: document.querySelector('#message_body').value
    })
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        document.querySelector('#message_body').value = ''
        load_room(id, true)
      } else {
        show_error(result['error']);
      }
    });
}

function join_room() {
  fetch('/join', {
    method: 'POST',
    body: JSON.stringify({
      name: document.querySelector('#room_name').value,
      password: document.querySelector('#password').value
    })
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        window.location.href = "/room/" + result['id'];
      } else {
        show_error(result['error'], false);
      }
    });
}

function join_open_room(name) {
  fetch('/join', {
    method: 'POST',
    body: JSON.stringify({
      name: name,
      password: ""
    })
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        window.location.href = "/room/" + result['id'];
      } else {
        show_error(result['error']);
      }
    });
}

function create_room() {
  fetch('/create', {
    method: 'POST',
    body: JSON.stringify({
      name: document.querySelector('#room_name').value,
      password: document.querySelector('#password').value
    })
  })
    .then(response => response.json())
    .then(result => {
      if (!result['error']) {
        window.location.href = "/room/" + result['id'];
      } else {
        show_error(result['error']);
      }
    });
}