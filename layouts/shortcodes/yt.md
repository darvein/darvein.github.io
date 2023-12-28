{{ $id := .Get "id"}}

<div class="google-video">
<iframe 
width="95%"
height="520"
src="https://www.youtube-nocookie.com/embed/{{ .Get `id` }}"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
