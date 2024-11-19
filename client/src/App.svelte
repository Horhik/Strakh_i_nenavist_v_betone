<script>
  import { onMount } from "svelte";

  let objects = [];
  let selectedObject = null;
  let materials = [];
  let selectedMaterial = null;
  let defects = [];
  let selectedDefect = null;

  // Запрашиваем список объектов при загрузке страницы
  onMount(async () => {
    const response = await fetch("/api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action_type: "request_objects", query: "all" }),
    });
    const data = await response.json();
    objects = data.objects || [];
  });

  // Обработчик выбора объекта
  async function selectObject(event) {
    selectedObject = event.target.value;
    selectedMaterial = null; // Сбрасываем выбранный материал
    selectedDefect = null; // Сбрасываем выбранный дефект
    defects = []; // Очищаем список дефектов

    const response = await fetch("/api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_type: "request_materials",
        query: selectedObject,
      }),
    });
    const data = await response.json();
    materials = data.materials || [];
  }

  // Обработчик выбора материала
  async function selectMaterial(event) {
    selectedMaterial = event.target.value;
    selectedDefect = null; // Сбрасываем выбранный дефект

    const response = await fetch("/api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_type: "request_defects",
        query: [selectedObject, selectedMaterial],
      }),
    });
    const data = await response.json();
    defects = data.defects || [];
  }

  // Обработчик выбора дефекта
  function selectDefect(event) {
    selectedDefect = event.target.value;
  }
</script>

<main>
  <h1>Выбор данных</h1>

  <!-- Селектор объектов -->
  {#if objects.length > 0}
    <label for="object-select">Выберите объект:</label>
    <select id="object-select" on:change={selectObject}>
      <option value="" disabled selected>Выберите объект</option>
      {#each objects as object}
        <option value={object.id}>{object.name}</option>
      {/each}
    </select>
  {/if}

  <!-- Селектор материалов -->
  {#if selectedObject && materials.length > 0}
    <label for="material-select">Выберите материал:</label>
    <select id="material-select" on:change={selectMaterial}>
      <option value="" disabled selected>Выберите материал</option>
      {#each materials as material}
        <option value={material.id}>{material.name}</option>
      {/each}
    </select>
  {/if}

  <!-- Селектор дефектов -->
  {#if selectedMaterial && defects.length > 0}
    <label for="defect-select">Выберите дефект:</label>
    <select id="defect-select" on:change={selectDefect}>
      <option value="" disabled selected>Выберите дефект</option>
      {#each defects as defect}
        <option value={defect.id}>{defect.name}</option>
      {/each}
    </select>
  {/if}

  {#if selectedDefect}
    <p>Вы выбрали дефект: {selectedDefect}</p>
  {/if}
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    margin: 2em;
  }

  label, select, p {
    margin-bottom: 1em;
    display: block;
  }
</style>
