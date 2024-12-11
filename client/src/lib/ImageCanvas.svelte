<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';

    let canvas;
    let context;
    let images = $state([]);  // Array to hold multiple images
    let currentIndex = $state(0);  // Index to track the current image
    let showPopup = $state(false); // To control popup visibility
    let clickedDot = $state(null); // Store the clicked dot for the popup
    let {dots, onMarkersUpdated, onMarkerClicked} = $props()
    let paneCount = $derived(dots.length);

    $effect(() => {
        onMarkersUpdated(dots, currentIndex)
        drawCanvas();
        let dts = $state.snapshot(dots)
        console.log("DOTS! len", dts)
        
        console.log("DOTS! len", dts.length)
        console.log(Object.getOwnPropertyNames(dts).length)

    })
    
    const dispatch = createEventDispatcher();

    // Handles the file input change
    function handleImageLoad(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                const img = new Image();
                img.onload = () => {
                    images.push(img);  // Add image to the array
                    if (images.length === 1) {
                        // Set the first image immediately if it's the first one added
                        currentIndex = 0;
                        drawCanvas();
                    }
                };
                img.src = reader.result;
            };
            reader.readAsDataURL(file);
        }
    }

    // Draw the image and dots on the canvas
    function drawCanvas() {
        if (!canvas || !context || !images[currentIndex]) return;

        const image = images[currentIndex];
        const aspectRatio = image.width / image.height;
        const maxHeight = window.innerHeight * 0.5; // Limit to 50% of screen height
        const width = aspectRatio * maxHeight;

        canvas.width = width;
        canvas.height = maxHeight;

        // Clear canvas
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the image
        context.drawImage(image, 0, 0, width, maxHeight);

        // Draw dots
        for (const dot of dots[currentIndex]) {
            context.beginPath();
            
         
            if (dot.highlight){
                context.beginPath();

                context.arc(dot.x * canvas.width, dot.y * canvas.height, 25, 0, 2 * Math.PI);
                context.fillStyle = "black"
                context.fill();

            }
            context.beginPath();

            context.arc(dot.x * canvas.width, dot.y * canvas.height, 20, 0, 2 * Math.PI);
            context.fillStyle = dot.color || 'blacku';
            context.fill();
        }
    }

    // Add a dot where the user clicks
    function handleCanvasClick(event) {
        const rect = canvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width;
        const y = (event.clientY - rect.top) / rect.height;
        const radius = 0.05
        // Check if clicked on a dot
        console.log("DOT: ", dots[currentIndex])
        console.log("X: ", x, "Y: ", y)
        const clicked = dots[currentIndex].find(dot => {
            return Math.abs(dot.x - x) < radius && Math.abs(dot.y - y) < radius;
        });

        if (clicked) {
            clickedDot = clicked;
            onMarkerClicked(x, y, currentIndex, true)
            showPopup = true;
        } else {
            onMarkerClicked(x, y, currentIndex, false)

            dots = { ...dots, [currentIndex]: [...dots[currentIndex], { x, y }] };
            drawCanvas();
        }
    }

    // Close the popup
    function closePopup() {
        showPopup = false;
        clickedDot = null;
    }

    // Switch to the next image in the array
    function nextImage() {
        if (images.length > 1) {
            currentIndex = (currentIndex + 1) % images.length;
            dots = { ...dots, [currentIndex]: dots[currentIndex] || [] };

            drawCanvas();
        }
    }

    // Switch to the previous image in the array
    function prevImage() {
        if (images.length > 1) {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            dots = { ...dots, [currentIndex]: dots[currentIndex] || [] };
            drawCanvas();
        }
    }

    // Initialize the canvas context
    onMount(() => {
        if (canvas) {
            context =  canvas.getContext('2d');
        }
    });
</script>

<style>
    .canvas-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }

    .canvas-container canvas {
        border: 1px solid #ccc;
        cursor: crosshair;
        max-width: 100%;
    }

    .upload-btn {
        margin: 10px 0;
    }

    .controls {
        margin-top: 10px;
    }
  
    button {
        padding: 10px;
        margin: 0 5px;
        cursor: pointer;
    }

    /* Popup Styles */
    .popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        border: 1px solid #ccc;
        padding: 20px;
        z-index: 100;
    }

    .popup button {
        margin-top: 10px;
    }

    .popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 99;
    }
    .upload-btn{
        width: auto;
    }   
</style>

<div class="canvas-container">
    <!-- Image Loader -->
     <div style="display: flex; align-items: center;">
         <!-- Navigation buttons -->
    <div class="controls">
        <button onclick={prevImage} disabled={images.length <= 1}>Previous</button>
        <button onclick={nextImage} disabled={images.length <= 1}>Next</button>
    </div>
    <input
      type="file"
      accept="image/*"
      class="upload-btn"
      onchange={handleImageLoad}
    />

   
    </div>
    <!-- Canvas -->
    <canvas bind:this={canvas} onclick={handleCanvasClick}></canvas>

    
</div>


