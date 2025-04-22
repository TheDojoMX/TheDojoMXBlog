---
short_name: fzavala
name: Francisco Zavala
position: Ingeniero de software apasionado de los algoritmos y las matemáticas aplicadas.
layout: single
---

<h2>Posts</h2>
<ul>
  {% assign filtered_posts = site.posts | where: 'author', page.name %}
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
