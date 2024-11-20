<script>
  import { onMount } from "svelte";

  let objects = [];
  let selectedObject = null;
  let materials = [];
  let selectedMaterial = null;
  let defects = [];
  let selectedDefect = null;
  let defectParams = null;
  let inputValue = "";
  let evaluationColor = null;

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
    selectedMaterial = null;
    selectedDefect = null;
    defectParams = null;
    inputValue = "";
    evaluationColor = null;
    defects = [];
    materials = [];

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
    selectedDefect = null;
    defectParams = null;
    inputValue = "";
    evaluationColor = null;
    defects = [];

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
  async function selectDefect(event) {
    selectedDefect = event.target.value;
    inputValue = "";
    evaluationColor = null;

    const response = await fetch("/api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_type: "request_params",
        query: selectedDefect,
      }),
    });
    const data = await response.json();
    console.log(data)
    defectParams = data || null;
  }

  // Обработчик ввода значения в поле
  function handleInput(event) {
    console.log("PRINTING")
    inputValue = parseFloat(event.target.value) || 0;
    evaluationColor = getEvaluationColor(inputValue, defectParams?.оценка);
  }

  // Определение цвета оценки
  function getEvaluationColor(value, оценка) {
    let maxval = Object.entries(оценка)[4][1][1]
    if(maxval < value){
                return("red")
    }

    if (value === "") return null;
    if (!оценка) return null;
    for (const [key, range] of Object.entries(оценка)) {
      const [min, max] = range;
      if (value >= min && value < max) {
        return getColorByGrade(parseInt(key));
      }
    }
  }


  // Возвращаем цвет в зависимости от оценки
  function getColorByGrade(grade) {
    switch (grade) {
      case 1: return "green";
      case 2: return "yellowgreen";
      case 3: return "yellow";
      case 4: return "orange";
      case 5: return "red";
      default: return null;
    }
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

  <!-- Поле ввода параметра дефекта -->
  {#if defectParams}
    <label for="defect-input">{defectParams.name} в единицах измерения({defectParams.measure}):</label>
    <input
      id="defect-input"
      type="number"
      placeholder={`в единицах измерения ${defectParams.measure}`}
      on:input={handleInput}
    />
    {#if evaluationColor}
      <span
        style="display: inline-block; position: absolute; width: 20px; height: 20px; border-radius: 50%; margin-left: 10px; background-color: {evaluationColor};"
      ></span>
    {/if}
  {/if}
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    margin: 2em;
  }

  label, select, input, p {
    margin-bottom: 1em;
    display: block;
  }

  input {
    padding: 0.5em;
    font-size: 1em;
  }
</style>
