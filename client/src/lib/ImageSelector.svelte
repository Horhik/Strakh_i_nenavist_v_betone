<script>
  import Marker from './Marker.svelte';
  import { writable } from 'svelte/store';

  let images = $state([]);
  let currentIndex = $state(0);
  let imageMarkers = $state({});
  let {kek, onUpdate} = $props()
  let imageContainer;

  // State for marker popup
  let popupVisible = writable(false);
  let clickedMarker = writable(null);

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
    const { offsetX, offsetY } = event;
    const x = (offsetX + imageContainer.getBoundingClientRect().left / 2) / imageContainer.getBoundingClientRect().width * 100;
    const y = (offsetY + imageContainer.getBoundingClientRect().top / 2) / imageContainer.getBoundingClientRect().height * 100;

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

  // Handle marker click
  function handleMarkerClick(marker) {
    clickedMarker.set(marker);
    popupVisible.set(true);
  }

  // Close popup
  function closePopup() {
    popupVisible.set(false);
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
      <div class="image_container" bind:this={imageContainer}>
        <div class="highlight-container"></div>

        <img src={images[currentIndex]} alt="Loaded image" class="image_display" onclick={addMarker} />
        <div class="highlight-image"></div>

        {#each imageMarkers[currentIndex] || [] as { x, y }, index}
          <Marker {x} {y} on:click={() => handleMarkerClick({ x, y })} />
        {/each}
      </div>

      <div class="image_controls">
        <button class="image_prev" onclick={prevImage} aria-label="Previous image">Prev</button>
        <button class="remove_marker" onclick={removeLastMarker} aria-label="Remove last marker">Remove Last Marker</button>
        <button class="image_next" onclick={nextImage} aria-label="Next image">Next</button>
      </div>

      <div class="image_info">
        Image {currentIndex + 1} of {images.length} (Markers: {(imageMarkers[currentIndex] || []).length})
      </div>

    </div>

    <!-- Popup Modal -->
    {#if $popupVisible}
      <div class="popup">
        <div class="popup-content">
          <p>Marker clicked at position: X: {$clickedMarker.x}, Y: {$clickedMarker.y}</p>
          <button onclick={closePopup}>Close</button>
        </div>
      </div>
    {/if}

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

  .highlight-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 0, 0.2); /* Transparent yellow */
    border: 2px solid rgba(255, 255, 0, 0.8); /* Yellow border */
    pointer-events: none; /* Ignore clicks */
  }

  .highlight-image {
    position: absolute;
    border: 10px solid rgba(0, 155, 0, 0.8); /* Green border */
    pointer-events: none; /* Ignore clicks */
  }

  /* Popup Styles */
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }
</style>
