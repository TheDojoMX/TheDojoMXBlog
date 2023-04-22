---
short_name: alexs
name: Alejandro Santamaría
position: Engineering Manager en Platzi
layout: single
---


<h2>Posts</h2>
<ul>
  {% assign filtered_posts = site.posts | where: 'author', page.name %}
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
