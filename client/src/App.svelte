<script>
  import ImageSelector from './lib/ImageSelector.svelte';
  import DeffectSelector from './lib/DeffectSelector.svelte';
  import { writable } from 'svelte/store';
  let kek= $state(0)

  let dots=$state([])
  let handleKek = nval => {
    kek = nval
    dots.push(kek)
  }


</script>

<main>
<ImageSelector {kek} onUpdate={handleKek}/>
<section>
{#each dots as { x, y }}
  <DeffectSelector/>
{/each}
</section>
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    justify-content: space-around;
  }

  label, select, input {
    margin-bottom: 1em;
    display: block;
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

.image_selector{
  margin: 0;
  padding: 0;
}

.main_container{
  display: flex;
}
</style>
