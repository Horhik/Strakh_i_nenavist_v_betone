<script>

  import { onMount } from "svelte";
  let {paneIndex, index, setColor, doHighlight} = $props();
  let objects = $state([]);
  let selectedObject = $state(null);
  let materials = $state([]);
  let selectedMaterial = $state(null);
  let defects = $state([]);
  let selectedDefects = $state([]);
  let defectParamsList = $state([]); // Список параметров для всех выбранных дефектов
  let higlightMarker = (should_i) => {
    console.log("HIGHLIGHTING MARKER")
    doHighlight(paneIndex, index, should_i)
  }
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
    selectedDefects = [];
    defectParamsList = [];
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
    selectedDefects = [];
    defectParamsList = [];
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
    const defectId = event.target.value;

    // Проверяем, если дефект уже выбран
    if (selectedDefects.includes(defectId)) return;

    selectedDefects = [...selectedDefects, defectId];

    const response = await fetch("/api", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_type: "request_params",
        query: defectId,
      }),
    });
    const data = await response.json();

    if (data) {
      defectParamsList = [
        ...defectParamsList,
        {
          defectId,
          name: data.name,
          measure: data.measure,
          оценка: data.оценка,
          inputValue: "",
          evaluationColor: null,
        },
      ];
    }
  }

  // Обработчик ввода значения в поле
  function handleInput(index, value) {
    defectParamsList = defectParamsList.map((item, i) => {
      if (i === index) {
        const evaluationColor = getEvaluationColor(value, item.оценка);
        setColor(evaluationColor);
        return { ...item, inputValue: value, evaluationColor };
      }
      return item;
    });
  }

  // Определение цвета оценки
  function getEvaluationColor(value, оценка) {
    if (value === "") return null;
    if (!оценка) return null;
    for (const [key, range] of Object.entries(оценка)) {
      const [min, max] = range;
      if (value >= min && value < max) {
        return getColorByGrade(parseInt(key));
      }
    }
    return "red"; // Если значение выходит за пределы
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
<div class="defect_selector obj-selector"
  onmouseenter={() => higlightMarker(true)}
  onmouseleave={() => higlightMarker(false)}
>
  <!-- Селектор объектов -->
  {#if objects.length > 0}
  <section >
    <label for="object-select">Выберите объект:</label>
    <select id="object-select" onchange={selectObject}>
      <option value="" disabled selected>Выберите объект</option>
      {#each objects as object}
        <option value={object.id}>{object.name}</option>
      {/each}
    </select>
    </section>
  {/if}

  <!-- Селектор материалов -->
  {#if selectedObject && materials.length > 0}

  <section>
    <label for="material-select">Выберите материал:</label>
    <select id="material-select" onchange={selectMaterial}>
      <option value="" disabled selected>Выберите материал</option>
      {#each materials as material}
        <option value={material.id}>{material.name}</option>
      {/each}
    </select>
  </section>
  {/if}

  <!-- Селектор дефектов -->
  {#if selectedMaterial && defects.length > 0}
  <section>
    <!-- <label for="defect-select">Выберите дефект:</label> -->
    <select id="defect-select" onchange={selectDefect}>
      <option value="" disabled selected>Выберите дефект</option>
      {#each defects as defect}
        <option value={defect.id}>{defect.name}</option>
      {/each}
    </select>
  </section>
  {/if}

  <section>
  <!-- Параметры дефектов -->
  {#each defectParamsList as defectParam, index}
    <div>
      <label for="input-{index}">
        {defectParam.name} в единицах измерения ({defectParam.measure}):
      </label>
      <div>
      <input
        id="input-{index}"
        type="number"
        placeholder={`в единицах измерения ${defectParam.measure}`}
        oninput={(e) => handleInput(index, parseFloat(e.target.value))}
      />
      <!-- {#if defectParam.evaluationColor}
        <span
          style="display: inline-block; position: relative; width: 20px; height: 20px; left: 45px; bottom: 45px;  border-radius: 50%; margin-left: 10px; background-color: {defectParam.evaluationColor};"
        ></span>
      {/if} -->
        </div>
    </div>
  {/each}

  </section>
</div>

<style>

  .defect_selector {
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 20px 0px;
    box-sizing: border-box;
    background-color: #445;
    margin: 10px;
    color: white;
    margin: 0 auto;
  }
  .defect_selector:hover {
    background-color: #334;
  }
  .obj-selector label{
    color: white;
  }

  .obj-selector option, .obj-selector select{
    color: white;
    background-color: #334;
  }
</style>