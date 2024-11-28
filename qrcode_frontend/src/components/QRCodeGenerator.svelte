<script lang="ts">
  import { QR_TYPES, getInputFields } from "../lib/qrFields";
  import { generateQRCode } from "../services/qrService";
  import type { FormData } from "../types/qr";

  let selectedType = "url";
  let qrCodeImage: string | null = null;
  let downloadEnabled = false;
  let formData: FormData = {};

  async function handleGenerateQRCode() {
    try {
      const blob = await generateQRCode(selectedType, formData);
      qrCodeImage = URL.createObjectURL(blob);
      downloadEnabled = true;
    } catch (error) {
      console.error("Error generating QR code:", error);
      alert(
        error instanceof Error
          ? error.message
          : "Failed to generate QR code. Please try again."
      );
    }
  }

  function handleTypeChange(newType: string) {
    selectedType = newType;
    formData = {};
    qrCodeImage = null;
    downloadEnabled = false;
  }

  function downloadQRCode(format: "png" | "svg") {
    if (!qrCodeImage) return;

    const link = document.createElement("a");
    link.href = qrCodeImage;
    link.download = `qr-code-${Date.now()}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
</script>

<div class="px-4 py-12 text-gray-800">
  <div class="container mx-auto">
    <!-- <h1
      class="text-4xl font-bold mb-12 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600"
    >
      QR Code Generator
    </h1> -->

    <!-- Tabs 요소로 변경된 QR Type Selection -->
    <div class="max-w-5xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">

      <!-- Tabs -->
      <div class="text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700">
        <ul class="flex flex-wrap -mb-px">
          {#each QR_TYPES as type}
            <li class="me-2">
              <a
                href="#"
                class={`inline-block p-4 rounded-t-lg ${
                  selectedType === type.value
                    ? "text-blue-600 border-b-2 border-blue-600"
                    : "border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300"
                }`}
                aria-current={selectedType === type.value ? "page" : undefined}
                on:click|preventDefault={() => handleTypeChange(type.value)}
              >
                {type.label}
              </a>
            </li>
          {/each}
        </ul>
      </div>


      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 p-8">
        <!-- Styles and 기타 섹션 유지 -->
        <div class="md:col-span-2">
          <h2 class="text-2xl font-semibold mb-6 text-gray-700">
            Styles
          </h2>
          <!-- Styles custom radio -->
          <div class="flex space-x-4">
            <!-- Option 1 -->
            <label class="block cursor-pointer">
              <input type="radio" name="custom-radio" class="hidden peer" />
              <div
                class="w-32 h-40 border border-gray-300 rounded-lg overflow-hidden shadow-md peer-checked:border-blue-500 peer-checked:ring-2 peer-checked:ring-blue-300"
              >
                <img
                  src="https://via.placeholder.com/128x160"
                  alt="Option 1"
                  class="w-full h-2/3 object-cover"
                />
                <div
                  class="h-1/3 bg-white flex items-center justify-center text-sm font-semibold text-gray-700"
                >
                  Option 1
                </div>
              </div>
            </label>

            <!-- Option 2 -->
            <label class="block cursor-pointer">
              <input type="radio" name="custom-radio" class="hidden peer" />
              <div
                class="w-32 h-40 border border-gray-300 rounded-lg overflow-hidden shadow-md peer-checked:border-blue-500 peer-checked:ring-2 peer-checked:ring-blue-300"
              >
                <img
                  src="https://via.placeholder.com/128x160"
                  alt="Option 2"
                  class="w-full h-2/3 object-cover"
                />
                <div
                  class="h-1/3 bg-white flex items-center justify-center text-sm font-semibold text-gray-700"
                >
                  Option 2
                </div>
              </div>
            </label>
          </div>

          <!-- Colors 섹션 유지 -->
          <h2 class="text-2xl font-semibold mb-6 text-gray-700">Colors</h2>
          <div class="space-y-5">
            <!-- Hex Color Input with Color Picker -->
            <div class="flex items-center gap-4">
              <div class="relative flex items-center gap-2">
                <input
                  type="text"
                  name="colorHex"
                  bind:value={formData.colorHex}
                  class="input input-bordered w-32 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="#000000"
                />
                <div class="relative">
                  <div
                    class="w-10 h-10 border border-gray-300 rounded-lg hover:ring-2 hover:ring-blue-300 transition-all cursor-pointer"
                    style="background-color: {formData.colorHex || '#ffffff'}"
                  ></div>
                  <input
                    type="color"
                    bind:value={formData.colorHex}
                    class="absolute inset-0 opacity-0 cursor-pointer w-10 h-10"
                  />
                </div>
              </div>
            </div>

            <!-- Predefined Colors -->
            <div class="grid grid-cols-4 gap-4">
              {#each ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"] as color}
                <label class="block cursor-pointer">
                  <input
                    type="radio"
                    name="predefined-color"
                    value={color}
                    bind:group={formData.colorHex}
                    class="hidden peer"
                  />
                  <div
                    class="w-10 h-10 border border-gray-300 rounded-lg overflow-hidden shadow-md peer-checked:border-blue-500 peer-checked:ring-2 peer-checked:ring-blue-300"
                    style="background-color: {color}"
                  ></div>
                </label>
              {/each}
            </div>
          </div>

          <!-- Input Form 섹션 유지 -->
          <form
            on:submit|preventDefault={handleGenerateQRCode}
            class="space-y-5"
          >
            {#each getInputFields(selectedType) as field}
              <div class="form-control">
                <label class="label" for="{field.name}-input">
                  <span class="label-text font-medium text-gray-700">
                    {field.label}
                    {#if field.required}
                      <span class="text-red-500">*</span>
                    {/if}
                  </span>
                </label>

                {#if field.type === "textarea"}
                  <textarea
                    id="{field.name}-input"
                    name={field.name}
                    bind:value={formData[field.name]}
                    required={field.required}
                    class="textarea textarea-bordered w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    rows="3"
                  ></textarea>
                {:else if field.type === "select"}
                  <select
                    id="{field.name}-input"
                    name={field.name}
                    bind:value={formData[field.name]}
                    required={field.required}
                    class="select select-bordered w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    {#each field.options ?? [] as option}
                      <option value={option.value}>{option.label}</option>
                    {/each}
                  </select>
                {:else}
                  <input
                    id="{field.name}-input"
                    type={field.type}
                    name={field.name}
                    bind:value={formData[field.name]}
                    required={field.required}
                    step={field.step}
                    min={field.min}
                    max={field.max}
                    class="input input-bordered w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                {/if}
              </div>
            {/each}

            <button
              type="submit"
              class="btn w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white border-0 shadow-lg"
            >
              Generate QR Code
            </button>
          </form>
        </div>

        <!-- QR Code Display 섹션 유지 -->
        <div class="md:col-span-1">
          <div class="sticky top-4">
            <h2 class="text-2xl font-semibold mb-6 text-gray-700">
              Generated QR Code
            </h2>
            <div class="bg-gray-50 p-6 rounded-xl border-2 border-gray-100">
              {#if qrCodeImage}
                <div class="aspect-square w-full mb-6">
                  <img
                    src={qrCodeImage}
                    alt="Generated QR Code"
                    class="w-full h-full object-contain"
                  />
                </div>
                <div class="space-y-3">
                  <button
                    on:click={() => downloadQRCode("png")}
                    disabled={!downloadEnabled}
                    class="btn btn-secondary w-full bg-blue-600 hover:bg-blue-700 text-white border-0"
                  >
                    Download PNG
                  </button>
                  <button
                    on:click={() => downloadQRCode("svg")}
                    disabled={!downloadEnabled}
                    class="btn w-full bg-white hover:bg-gray-50 text-blue-600 border-2 border-blue-600"
                  >
                    Download SVG
                  </button>
                </div>
              {:else}
                <div
                  class="aspect-square w-full flex items-center justify-center text-gray-400 bg-gray-100 rounded-lg"
                >
                  <div class="text-center">
                    <svg
                      class="w-16 h-16 mx-auto mb-4 text-gray-300"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 4v16m8-8H4"
                      ></path>
                    </svg>
                    <p>QR code will appear here<br />after generation</p>
                  </div>
                </div>
              {/if}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  :global(.form-radio) {
    width: 1.2rem;
    height: 1.2rem;
    border-radius: 50%;
    border: 2px solid #d1d5db;
    transition: all 0.2s ease;
  }
  :global(.form-radio:checked) {
    border-color: #2563eb;
    background-color: #2563eb;
  }
  :global(.btn:disabled) {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
