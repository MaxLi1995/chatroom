document.addEventListener('DOMContentLoaded', function() {
    let id = document.URL.match(/[0-9]+$/);
    load_followed_post(id, 1);


})

function load_followed_post(id, page) { 
  
    fetch('/followpost/' + id + '/' + page)
    .then(response => response.json())
    .then(object => {

      console.log(object);
      posts = object.posts;
  
      let text = "";
      for (let i in posts) {
          text += `<div class='item'><a href='/profilepage/${posts[i].posterid}'><h3>${posts[i].poster}</h3></a>
          <div id='editform${posts[i].id}' style='display:none'>
          <textarea class="form-control" id="editbody${posts[i].id}" style="padding:10px;resize:none;">${posts[i].body}</textarea>
          <button class="btn btn-primary" onclick='edit(${posts[i].id})' style="margin:5px;">Edit</button>
          </div>
          <div id='section${posts[i].id}'>
          <p id='body${posts[i].id}'>${posts[i].body}</p>
          <p style='color:grey;'>${posts[i].timestamp}</p>
          <div style='display:flex;'><div class='like' onclick='like(${posts[i].id}, ${id}, ${page})'>💖</div><div id='like${posts[i].id}'> ${posts[i].liker}</div></div>
          </div>
          </div>`;
      };

      if (object.hasnextpage && object.haspreviouspage){
        text += `<div style='display:flex;'><div class="btn btn-primary" id='back' onclick='load_followed_post(${id}, ${page-1})'>Previous</div>
          <div class="btn btn-primary" id='next' onclick='load_followed_post(${id}, ${page+1})'>Next</div></div>`
      } else if (object.hasnextpage){
        text += `<div style='display:flex;'><div class="btn btn-primary" id='next' onclick='load_followed_post(${id}, ${page+1})'>Next</div></div>`
      } else if (object.haspreviouspage){
        text += `<div style='display:flex;'><div class="btn btn-primary"id='back' onclick='load_followed_post(${id}, ${page-1})'>Previous</div></div>`
      } 
      document.getElementById("followed-posts").innerHTML = text;
  
    });
}

function like(post_id, id, page){
  fetch('/like/' + post_id , {
      method: 'PUT'
  });
  load_followed_post(id, page);
}