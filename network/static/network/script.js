document.addEventListener('DOMContentLoaded', function() {

    load_post(1);

    
    document.querySelector('#newpost-form').onsubmit = () => {

        newpost();
        
      };
    
})

function load_post(page) { 
  
    fetch('/posts/' + page)
    .then(response => response.json())
    .then(response => {
      let posts = response.posts;

      console.log(response);
  
      let text = "";
      for (let i in posts) {
          text += `<div class='item'><a href='/profilepage/${posts[i].posterid}'><h3>${posts[i].poster}</h3></a>`;
          if (posts[i].self_post){
            text += `<a id='edit${posts[i].id}' onclick='showedit(${posts[i].id})' style='color:blue;'>edit</a>`;
          };
          text += `<div id='editform${posts[i].id}' style='display:none'>
          <textarea class="form-control" id="editbody${posts[i].id}" style="padding:10px;resize:none;">${posts[i].body}</textarea>
          <button class="btn btn-primary" onclick='edit(${posts[i].id})' style="margin:5px;">Edit</button>
          </div>
          <div id='section${posts[i].id}'>
          <p id='body${posts[i].id}'>${posts[i].body}</p>
          <p style='color:grey;'>${posts[i].timestamp}</p>
          <div style='display:flex;'><div class='like' onclick='like(${posts[i].id}, ${page})'>💖</div><div id='like${posts[i].id}'> ${posts[i].liker}</div></div>
          </div>
          </div>`;
      }
      if (response.hasnextpage && response.haspreviouspage){
        text += `<div style='display:flex;'><div class="btn btn-primary" id='back' onclick='load_post(${page-1})'>Previous</div>
          <div class="btn btn-primary" id='next' onclick='load_post(${page+1})'>Next</div></div>`
      } else if (response.hasnextpage){
        text += `<div style='display:flex;'><div class="btn btn-primary" id='next' onclick='load_post(${page+1})'>Next</div></div>`
      } else if (response.haspreviouspage){
        text += `<div style='display:flex;'><div class="btn btn-primary"id='back' onclick='load_post(${page-1})'>Previous</div></div>`
      } 


      document.getElementById("posts").innerHTML = text;
  
    });
}

function newpost() {
    fetch('/compose', {
    
      method: 'POST',
      body: JSON.stringify({
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
    window.location.reload(true);
}

function edit(id){
    fetch('/edit/' + id , {
      method: 'PUT',
      body: JSON.stringify({
          body: document.getElementById('editbody' + id).value
      })
    });
    document.getElementById('body' + id).innerHTML = document.getElementById('editbody' + id).value
    document.getElementById('editform'+id).style.display = 'none';
    document.getElementById('section'+id).style.display = 'block';
}

function showedit(id){
    document.getElementById('editform'+id).style.display = 'block';
    document.getElementById('section'+id).style.display = 'none';
}

async function like(post_id, page){
    fetch('/like/' + post_id , {
      method: 'PUT'
    });
    load_post(page);
}
