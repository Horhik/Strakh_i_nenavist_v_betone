<script>
  import ImageSelector from './lib/ImageSelector.svelte';
  import ImageCanvas from './lib/ImageCanvas.svelte';
  import DeffectSelector from './lib/DeffectSelector.svelte';
  import { writable } from 'svelte/store';


  let paneIndex = $state(0);
  let dots=$state([[]])
  let selectorList = $state([[]])
  let onMarkersUpdated = (new_dots, currentIndex) => {
    dots = new_dots; 
    console.log("CURRENT INDEX", currentIndex)
    paneIndex = currentIndex
  }

  let doHighlight = (pane, index, should) => {
    console.log("DO HIGHLIGHT", pane, index, should)
    dots[pane][index].highlight = should;
  }
  let onMarkerClicked = (x, y, pane, itWas) => {
    
    console.log("CLIC", $state.snapshot(dots))
    console.log("CLIC", $state.snapshot(dots)[0])
    console.log("CLIC vals", Object.values($state.snapshot(dots)))
    console.log("CLIC keys", Object.keys($state.snapshot(dots)))

    if(itWas) {
       console.log("IT WAS")
       let dotIndex = dots[pane].findIndex(obj => Math.abs(obj.x - x) < 0.05 && Math.abs(obj.y - y) < 0.05);
        console.log("DOT INDEX", dotIndex)
       console.log("DOTS", dots[pane][dotIndex])
       dots[pane][dotIndex].color = 'green'
       console.log("selector", selectorList[pane][dotIndex])
       selectorList[pane][dotIndex].scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      console.log("IT WASN't")
    } 
  }

  let setEvaluationColor = (pane, index, color) => {
    console.log("SET EVALUATION COLOR", pane, index, color)
    dots[pane][index].color = color;
  }


</script>

<main>
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
>
<!-- <ImageSelector {kek} onUpdate={handleKek}/> -->
 <ImageCanvas {dots} {onMarkersUpdated} {onMarkerClicked}/>
<section class="defects">
  {#each Object.values($state.snapshot(dots))[paneIndex] as dot, index}
    <DeffectSelector {paneIndex} {index} bind:this={selectorList[paneIndex][index]} setColor={(color) => setEvaluationColor(paneIndex, index, color)} {doHighlight}/>
  {/each}
</section>
</main>

<style>

  body {
    background-color: #333 !important;
  }
  main {
    font-family: Arial, sans-serif;
    justify-content: space-around;
  }

  label, select, input {
    margin-bottom: 1em;
    display: block;
  }
  label {
    color: white;
  }

  input {
    padding: 0.5em;
    font-size: 1em;
  }
section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.defects {

    display: grid;
    grid-template-columns: repeat(3, minmax(0, 0.5fr));
    grid-gap: 12px;
    margin: 0 100px;

    margin-top: 20px;
}


.image_selector{
  margin: 0;
  padding: 0;
}

.main_container{
  display: flex;
}



</style>
