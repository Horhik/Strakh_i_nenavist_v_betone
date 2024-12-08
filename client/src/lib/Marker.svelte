<script>
  let {x, y} = $props()
</script>
<div
            class="marker"
            style="left: {x}%; top: {y}%;"
></div>

<style>
  .marker {
    position: absolute;
    width: 10px;
    height: 10px;
    background-color: red;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }
  </style>
