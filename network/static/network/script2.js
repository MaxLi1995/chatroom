document.addEventListener('DOMContentLoaded', function() {
    let id = document.URL.match(/[0-9]+$/);
    

    showprofile(id, 1);


})

function showprofile(id, page){

    fetch('/profile/' + id + '/' + page) 
    .then(response => response.json())
    .then(profile => {
  
        console.log(profile);
      
        let text = "";
        for (let i in profile.posts) {
            text += `<div id='${profile.posts[i].id}' class='item'>
            <div style='display:flex;'>
            <a onclick='showprofile(${profile.posts[i].posterid},1)'><h3>${profile.posts[i].poster}</h3></a></div>`
            if (profile.posts[i].self_post){
                text += `<a id='edit${profile.posts[i].id}' onclick='showedit(${profile.posts[i].id})' style='color:blue;'>edit</a>`;
              };
            text += `<div id='editform${profile.posts[i].id}' style='display:none'>
            <textarea class="form-control" id="editbody${profile.posts[i].id}" style="padding:10px;resize:none;">${profile.posts[i].body}</textarea>
            <button class="btn btn-primary" onclick='edit(${profile.posts[i].id})' style="margin:5px;">Edit</button>
            </div>
            <div id='section${profile.posts[i].id}'>
            <p id='body${profile.posts[i].id}'>${profile.posts[i].body}</p>
            <p style='color:grey;'>${profile.posts[i].timestamp}</p>
            <div style='display:flex;'><div class='like' onclick='like(${profile.posts[i].id}, ${id}, ${page})'>💖</div><div id='like${profile.posts[i].id}'> ${profile.posts[i].liker}</div></div>
            </div>
            </div>`;
        };
        followtext = '';
        if (!profile.is_me){
            if(profile.isFollowing){
                followtext += `<button onclick="follow(${profile.userid})" class="btn btn-primary" style="margin:5px;" >Unfollow</button>`
            } else { 
                followtext += `<button onclick="follow(${profile.userid})" class="btn btn-primary" style="margin:5px;" >Follow</button>`
            } 
         }

        document.getElementById("profile").innerHTML = `<div class='item'><div style='display:flex'>
        <h3>${profile.username}</h3>`+ followtext +`</div>
        <div>Follower: ${profile.followerCount}</div><div>Following: ${profile.followingCount}</div>
        </div>`;

        if (profile.hasnextpage && profile.haspreviouspage){
            text += `<div style='display:flex;'><div class="btn btn-primary" id='back' onclick='showprofile(${id}, ${page-1})'>Previous</div>
              <div class="btn btn-primary" id='next' onclick='showprofile(${id}, ${page+1})'>Next</div></div>`
          } else if (profile.hasnextpage){
            text += `<div style='display:flex;'><div class="btn btn-primary" id='next' onclick='showprofile(${id}, ${page+1})'>Next</div></div>`
          } else if (profile.haspreviouspage){
            text += `<div style='display:flex;'><div class="btn btn-primary"id='back' onclick='showprofile(${id}, ${page-1})'>Previous</div></div>`
          } 
    
      
        document.getElementById("profile_posts").innerHTML = text;
    });
  
}

function follow(id){
    fetch('/follow/' + id , {
        method: 'PUT'
    });
    window.location.reload(true);
}

function like(post_id, id, page){
    fetch('/like/' + post_id , {
        method: 'PUT'
    });
    showprofile(id, page);
}
  