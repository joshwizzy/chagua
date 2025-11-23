<template>
  <footer class="bg-gray-800 text-white py-12 mt-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
        <div>
          <h3 class="text-2xl font-bold mb-2 text-primary-400">{{ $t('app.name') }}</h3>
          <p class="text-gray-400">{{ $t('app.tagline') }}</p>
        </div>

        <div>
          <h4 class="font-semibold mb-4">Quick Links</h4>
          <ul class="space-y-2">
            <li><router-link to="/products" class="text-gray-400 hover:text-white transition-colors">Products</router-link></li>
            <li><router-link to="/about" class="text-gray-400 hover:text-white transition-colors">About Us</router-link></li>
            <li><router-link to="/contact" class="text-gray-400 hover:text-white transition-colors">Contact</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold mb-4">For Sellers</h4>
          <ul class="space-y-2">
            <li><router-link to="/register" class="text-gray-400 hover:text-white transition-colors">Become a Seller</router-link></li>
            <li><router-link to="/seller/dashboard" class="text-gray-400 hover:text-white transition-colors">Seller Dashboard</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold mb-4">Support</h4>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Help Center</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
            <li><a href="#" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
          </ul>
        </div>
      </div>

      <div class="border-t border-gray-700 pt-4 text-center text-gray-400">
        <p>&copy; 2025 CHAGUA. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>
