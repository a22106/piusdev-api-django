<script lang="ts">
  let qrImage: string = '';
  let text: string = '1234';

  async function fetchQRCode() {
    try {
      const response = await fetch(`http://localhost:8000/v1/qr/text/?text=${text}`);
      if (!response.ok) throw new Error('Failed to fetch QR code');
      const blob = await response.blob();
      qrImage = URL.createObjectURL(blob);
    } catch (error) {
      console.error('Error fetching QR code:', error);
    }
  }

  // Fetch QR code when component mounts
  fetchQRCode();
</script>

<div class="container">
  <h1>QR Code Generator</h1>
  <input
    type="text"
    bind:value={text}
    placeholder="Enter text"
    on:input={fetchQRCode}
  />
  {#if qrImage}
    <img src={qrImage} alt="QR Code" />
  {/if}
</div>

<style>
  .container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 1rem;
    text-align: center;
  }

  input {
    width: 100%;
    max-width: 300px;
    padding: 0.5rem;
    margin: 1rem 0;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  img {
    max-width: 200px;
    margin-top: 1rem;
  }

  h1 {
    color: #333;
    margin-bottom: 1rem;
  }
</style>