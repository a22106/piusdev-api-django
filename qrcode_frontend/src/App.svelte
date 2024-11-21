<script lang="ts">
  import QRCodeGenerator from "./components/QRCodeGenerator.svelte";
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  <!-- Navbar -->
  <nav class="bg-white shadow-md">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Logo/Brand -->
        <a href="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold text-gray-800">QR Code Generator</span>
        </a>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-4">
          <a
            href="/"
            class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
            >Home</a
          >
          <a
            href="/api"
            class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
            >API Documentation</a
          >
        </div>

        <!-- Auth Buttons -->
        <div class="flex items-center space-x-2">
          <a
            href="/signup"
            class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
            >Sign Up</a
          >
          <a
            href="/signin"
            class="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md text-sm font-medium"
            >Sign In</a
          >
        </div>
      </div>
    </div>
  </nav>

  <main>
    <QRCodeGenerator />
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      "Helvetica Neue", Arial, sans-serif;
    min-height: 100vh;
    background: linear-gradient(
      to bottom right,
      rgb(239, 246, 255),
      rgb(238, 242, 255)
    );
  }
</style>
