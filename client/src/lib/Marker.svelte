<script>
  let {x, y} = $props()
  function showProps(){
        console.log("SHOWING")
  }
</script>
<div
            class="marker"
            style="left: {x}%; top: {y}%;"
            onclick={showProps}
></div>

<style>
  .marker {
    z-index: 10000000;
    position: absolute;
    width: 30px;
    height: 30px;
    background-color: red;
    border-radius: 50%;
    transform: translate(-50%, -50%);
  }
  </style>
