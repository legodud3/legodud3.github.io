---
layout: page
title: My Blog
---

<style>
  .search-container {
    margin: 20px 0;
  }
  
  .search-input {
    width: 100%;
    max-width: 400px;
    padding: 10px;
    border: 2px solid #007acc;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .posts-list {
    margin-top: 30px;
  }
  
  .post-item {
    padding: 10px 0;
    border-bottom: 1px solid #eee;
    transition: background-color 0.2s;
  }
  
  .post-item:hover {
    background-color: #f5f5f5;
    padding-left: 5px;
  }
  
  .post-item a {
    color: #007acc;
    text-decoration: none;
    font-weight: 500;
  }
  
  .post-item a:hover {
    text-decoration: underline;
  }
  
  .post-date {
    color: #666;
    font-size: 14px;
    margin-left: 10px;
  }
  
  .no-posts {
    color: #999;
    font-style: italic;
    padding: 20px 0;
  }
</style>

<div class="search-container">
  <input 
    type="text" 
    id="searchInput" 
    class="search-input" 
    placeholder="Search posts by title..."
    autocomplete="off"
  >
</div>

<div class="posts-list">
  <div id="postsContainer">
    {% if site.posts.size == 0 %}
      <p class="no-posts">No posts yet. Check back soon!</p>
    {% else %}
      {% for post in site.posts %}
        <div class="post-item" data-title="{{ post.title | downcase }}">
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
        </div>
      {% endfor %}
    {% endif %}
  </div>
</div>

<script>
  document.getElementById('searchInput').addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const postItems = document.querySelectorAll('.post-item');
    
    postItems.forEach(item => {
      const title = item.getAttribute('data-title');
      if (title.includes(searchTerm)) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });
  });
</script>
