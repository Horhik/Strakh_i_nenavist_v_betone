<script>
  import Marker from './Marker.svelte';
  import { get, writable } from 'svelte/store';

  let images = $state([]);
  let currentIndex = $state(0);
  let imageMarkers = $state({});
  let {kek, onUpdate} = $props()

  function handleImageLoad(event) {
    const files = event.target.files;

    if (files && files.length > 0) {
      const newImages = [];
      for (const file of files) {
        newImages.push(URL.createObjectURL(file));
      }
      images = [...images, ...newImages];
      currentIndex = images.length - 1;
    }
  }

  function nextImage() {
    if (images.length > 0) {
      currentIndex = (currentIndex + 1) % images.length;
    }
  }

  function prevImage() {
    if (images.length > 0) {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
    }
  }

  function addMarker(event) {

    console.log("Kek is", kek)
    const imageContainer = event.currentTarget;
    const rect = imageContainer.getBoundingClientRect();

    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    onUpdate((x,y))

    if (!imageMarkers[currentIndex]) {
      imageMarkers[currentIndex] = [];
    }

    imageMarkers[currentIndex] = [...imageMarkers[currentIndex], { x, y }];
  }

  function removeLastMarker() {
    if (imageMarkers[currentIndex] && imageMarkers[currentIndex].length > 0) {
      imageMarkers[currentIndex] = imageMarkers[currentIndex].slice(0, -1);
    }
  }
</script>

<section class="image_selector">
  <input
    type="file"
    accept="image/*"
    multiple
    id="image-loader"
    style="display: none;"
    onchange={handleImageLoad}
  />

  <button
    onclick={() => document.getElementById('image-loader').click()}
    aria-label="Load images"
  >
    Load Images
  </button>

  {#if images.length > 0}

    <div class="image_carousel">

      <div
        class="image_container"
        onclick={addMarker}
      >

        <img
          src={images[currentIndex]}
          alt="Loaded image"
          class="image_display"
        />

        {#each imageMarkers[currentIndex] || [] as { x, y }}

         <Marker {x} {y}/>

        {/each}

      </div>

      <div class="image_controls">

        <button
          class="image_prev"
          onclick={prevImage}
          aria-label="Previous image"
        >
          Prev
        </button>

        <button
          class="remove_marker"
          onclick={removeLastMarker}
          aria-label="Remove last marker"
        >
          Remove Last Marker
        </button>

        <button
          class="image_next"
          onclick={nextImage}
          aria-label="Next image"
        >
          Next
        </button>

      </div>

      <div class="image_info">

        Image {currentIndex + 1} of {images.length}

        (Markers: {(imageMarkers[currentIndex] || []).length})

      </div>

    </div>

  {/if}

</section>

<style>
  .image_selector {

    display: flex;

    flex-direction: column;

    align-items: center;

    width: 100%;

    padding: 20px 0px;

    box-sizing: border-box;

  }

  

  .image_carousel {

    display: flex;

    flex-direction: column;

    align-items: center;

    width: 100%;

  }

  

  .image_container {

    position: relative;

    width: 100%;

    max-height: 50vh;

    display: flex;

    justify-content: center;

  }

  

  .image_display {

    max-width: 100%;

    max-height: 50vh;

    object-fit: contain;

  }

  

  

  .image_controls {

    display: flex;

    justify-content: center;

    margin-top: 10px;

    gap: 10px;

  }

  

  .image_info {

    margin-top: 10px;

    font-size: 0.9em;

    color: #666;

  }

  

  button {

    padding: 5px 10px;

    margin: 0 5px;

  }

</style>
