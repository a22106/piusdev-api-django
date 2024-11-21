<script lang="ts">
  import { onMount } from 'svelte';
  
  let selectedType = 'url';
  let qrCodeImage: string | null = null;
  let downloadEnabled = false;

  // API base URL
  const API_BASE_URL = 'http://localhost:8000/v1/qr';

  // QR code types
  const qrTypes = [
    { value: 'url', label: 'URL' },
    { value: 'text', label: 'Text' },
    { value: 'email', label: 'Email' },
    { value: 'phone', label: 'Phone Number' },
    { value: 'sms', label: 'SMS' },
    { value: 'wifi', label: 'WiFi' },
    { value: 'vcard', label: 'VCard' },
    { value: 'mecard', label: 'MeCard' },
    { value: 'geo', label: 'Location' },
    { value: 'event', label: 'Event' },
    { value: 'bitcoin', label: 'Bitcoin' },
    { value: 'whatsapp', label: 'WhatsApp' }
  ];

  interface InputField {
    name: string;
    type: string;
    label: string;
    required?: boolean;
    options?: { value: string; label: string }[];
    step?: string;
    min?: number;
    max?: number;
  }

  interface SelectOption {
    value: string;
    label: string;
  }

  // Form data
  let formData: { [key: string]: string } = {};

  async function generateQRCode() {
    try {
      // Adjust endpoint for phone number
      let endpoint = `${API_BASE_URL}/${selectedType === 'phone' ? 'phonenumber' : selectedType}/`;
      
      // Adjust form data based on type
      const adjustedFormData = { ...formData };
      
      // Handle special cases
      switch (selectedType) {
        case 'phone':
          adjustedFormData.phone_number = formData.phone;
          delete adjustedFormData.phone;
          break;
        case 'vcard':
          adjustedFormData.vcard_phone = formData.phone;
          adjustedFormData.vcard_mobile = formData.mobile;
          adjustedFormData.vcard_email = formData.email;
          adjustedFormData.vcard_url = formData.url;
          break;
        case 'event':
          if (adjustedFormData.start_date) {
            adjustedFormData.start_date = new Date(adjustedFormData.start_date).toISOString();
          }
          if (adjustedFormData.end_date) {
            adjustedFormData.end_date = new Date(adjustedFormData.end_date).toISOString();
          }
          break;
      }

      const queryParams = new URLSearchParams(adjustedFormData).toString();
      const fullUrl = `${endpoint}?${queryParams}`;
      
      console.log('Sending request to:', fullUrl);
      console.log('Form data:', adjustedFormData);
      
      const response = await fetch(fullUrl);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', {
          status: response.status,
          statusText: response.statusText,
          body: errorText
        });
        throw new Error(`Failed to generate QR code: ${response.status} ${response.statusText}\n${errorText}`);
      }

      const contentType = response.headers.get('content-type');
      console.log('Response content type:', contentType);

      const blob = await response.blob();
      if (blob.size === 0) {
        throw new Error('Received empty response from server');
      }

      qrCodeImage = URL.createObjectURL(blob);
      downloadEnabled = true;
    } catch (error) {
      console.error('Error generating QR code:', error);
      alert(error instanceof Error ? error.message : 'Failed to generate QR code. Please try again.');
    }
  }

  function downloadQRCode(format: 'png' | 'svg') {
    if (!qrCodeImage) return;

    const link = document.createElement('a');
    link.href = qrCodeImage;
    link.download = `qr-code-${Date.now()}.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function handleTypeChange() {
    formData = {};
    qrCodeImage = null;
    downloadEnabled = false;
  }

  function getInputFields(): InputField[] {
    switch (selectedType) {
      case 'url':
        return [{ 
          name: 'url', 
          type: 'text', 
          label: 'URL',
          required: true 
        }];
      
      case 'text':
        return [{ 
          name: 'text', 
          type: 'textarea', 
          label: 'Text',
          required: true 
        }];
      
      case 'email':
        return [
          { 
            name: 'email', 
            type: 'email', 
            label: 'Email Address',
            required: true 
          },
          { 
            name: 'subject', 
            type: 'text', 
            label: 'Subject' 
          },
          { 
            name: 'body', 
            type: 'textarea', 
            label: 'Message Body' 
          }
        ];
      
      case 'phone':
        return [{ 
          name: 'phone', 
          type: 'tel', 
          label: 'Phone Number',
          required: true 
        }];
      
      case 'vcard':
        return [
          { 
            name: 'first_name', 
            type: 'text', 
            label: 'First Name',
            required: true 
          },
          { 
            name: 'last_name', 
            type: 'text', 
            label: 'Last Name',
            required: true 
          },
          { 
            name: 'phone', 
            type: 'tel', 
            label: 'Phone Number' 
          },
          { 
            name: 'mobile', 
            type: 'tel', 
            label: 'Mobile Number',
            required: true 
          },
          { 
            name: 'email', 
            type: 'email', 
            label: 'Email',
            required: true 
          },
          { 
            name: 'url', 
            type: 'url', 
            label: 'Website' 
          },
          { 
            name: 'organization', 
            type: 'text', 
            label: 'Organization' 
          }
        ];
      
      case 'wifi':
        return [
          { 
            name: 'ssid', 
            type: 'text', 
            label: 'Network Name (SSID)',
            required: true 
          },
          { 
            name: 'password', 
            type: 'password', 
            label: 'Password' 
          },
          { 
            name: 'encryption', 
            type: 'select', 
            label: 'Encryption',
            options: [
              { value: 'WPA', label: 'WPA/WPA2' },
              { value: 'WEP', label: 'WEP' },
              { value: 'nopass', label: 'None' }
            ],
            required: true 
          }
        ];
      
      case 'sms':
        return [
          { 
            name: 'phone_number', 
            type: 'tel', 
            label: 'Phone Number',
            required: true 
          },
          { 
            name: 'message', 
            type: 'textarea', 
            label: 'Message' 
          }
        ];
      
      case 'geo':
        return [
          { 
            name: 'latitude', 
            type: 'number', 
            label: 'Latitude',
            required: true,
            step: 'any'
          },
          { 
            name: 'longitude', 
            type: 'number', 
            label: 'Longitude',
            required: true,
            step: 'any'
          },
          { 
            name: 'query', 
            type: 'text', 
            label: 'Place Name' 
          }
        ];
      
      case 'event':
        return [
          { 
            name: 'summary', 
            type: 'text', 
            label: 'Event Title',
            required: true 
          },
          { 
            name: 'start_date', 
            type: 'datetime-local', 
            label: 'Start Date',
            required: true 
          },
          { 
            name: 'end_date', 
            type: 'datetime-local', 
            label: 'End Date',
            required: true 
          },
          { 
            name: 'location', 
            type: 'text', 
            label: 'Location' 
          },
          { 
            name: 'description', 
            type: 'textarea', 
            label: 'Description' 
          }
        ];
      
      case 'whatsapp':
        return [
          { 
            name: 'phone_number', 
            type: 'tel', 
            label: 'Phone Number',
            required: true 
          },
          { 
            name: 'message', 
            type: 'textarea', 
            label: 'Message' 
          }
        ];
      
      case 'bitcoin':
        return [
          { 
            name: 'address', 
            type: 'text', 
            label: 'Bitcoin Address',
            required: true 
          },
          { 
            name: 'amount', 
            type: 'number', 
            label: 'Amount (BTC)',
            step: 'any'
          },
          { 
            name: 'label', 
            type: 'text', 
            label: 'Label' 
          },
          { 
            name: 'message', 
            type: 'text', 
            label: 'Message' 
          }
        ];
      
      default:
        return [];
    }
  }
</script>

<div class="px-4 py-12 text-gray-800">
  <div class="container mx-auto">
    <h1 class="text-4xl font-bold mb-12 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
      QR Code Generator
    </h1>
    
    <div class="max-w-5xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 p-8">
        <!-- QR Type Selection -->
        <div class="md:col-span-2">
          <h2 class="text-2xl font-semibold mb-6 text-gray-700">Select QR Code Type</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
            {#each qrTypes as type}
              <label class="flex items-center space-x-2 cursor-pointer hover:bg-blue-50 p-2 rounded-lg transition-colors">
                <input
                  type="radio"
                  name="qr_type"
                  value={type.value}
                  bind:group={selectedType}
                  on:change={handleTypeChange}
                  class="form-radio text-blue-600"
                />
                <span class="text-gray-700">{type.label}</span>
              </label>
            {/each}
          </div>

          <!-- Input Form -->
          <form on:submit|preventDefault={generateQRCode} class="space-y-5">
            {#each getInputFields() as field}
              <div class="form-control">
                <label class="label" for="{field.name}-input">
                  <span class="label-text font-medium text-gray-700">
                    {field.label}
                    {#if field.required}
                      <span class="text-red-500">*</span>
                    {/if}
                  </span>
                </label>
                
                {#if field.type === 'textarea'}
                  <textarea
                    id="{field.name}-input"
                    name={field.name}
                    bind:value={formData[field.name]}
                    required={field.required}
                    class="textarea textarea-bordered w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    rows="3"
                  ></textarea>
                {:else if field.type === 'select'}
                  <select
                    id="{field.name}-input"
                    name={field.name}
                    bind:value={formData[field.name]}
                    required={field.required}
                    class="select select-bordered w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    {#each (field.options ?? []) as option}
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

        <!-- QR Code Display -->
        <div class="md:col-span-1">
          <div class="sticky top-4">
            <h2 class="text-2xl font-semibold mb-6 text-gray-700">Generated QR Code</h2>
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
                    on:click={() => downloadQRCode('png')}
                    disabled={!downloadEnabled}
                    class="btn btn-secondary w-full bg-blue-600 hover:bg-blue-700 text-white border-0"
                  >
                    Download PNG
                  </button>
                  <button
                    on:click={() => downloadQRCode('svg')}
                    disabled={!downloadEnabled}
                    class="btn w-full bg-white hover:bg-gray-50 text-blue-600 border-2 border-blue-600"
                  >
                    Download SVG
                  </button>
                </div>
              {:else}
                <div class="aspect-square w-full flex items-center justify-center text-gray-400 bg-gray-100 rounded-lg">
                  <div class="text-center">
                    <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                    <p>QR code will appear here<br/>after generation</p>
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
