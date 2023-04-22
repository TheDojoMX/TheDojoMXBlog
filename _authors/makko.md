---
short_name: makko
name: Héctor Vela
position: Senior Developer en Wizeline
---


<h2>Posts</h2>
<ul>
  {% assign filtered_posts = site.posts | where: 'author', page.name %}
  {% for post in filtered_posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
