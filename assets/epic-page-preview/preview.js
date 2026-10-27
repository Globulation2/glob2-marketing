const hero = document.getElementById('hero');
for (const thumbnail of document.querySelectorAll('.thumb')) {
  thumbnail.addEventListener('click', () => {
    hero.src = thumbnail.dataset.image;
    hero.alt = thumbnail.dataset.alt;
    const previous = document.querySelector('.thumb.selected');
    previous?.classList.remove('selected');
    previous?.setAttribute('aria-pressed', 'false');
    thumbnail.classList.add('selected');
    thumbnail.setAttribute('aria-pressed', 'true');
  });
}
