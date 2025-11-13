# PWA Setup Instructions

## Icon Generation

To complete the PWA setup, you need to generate app icons in various sizes.

### Required Icon Sizes
- 72x72
- 96x96
- 128x128
- 144x144
- 152x152
- 192x192
- 384x384
- 512x512

### How to Generate Icons

1. **Create a source icon** (1024x1024 recommended) with your CHAGUA logo
2. **Use an online tool** like:
   - https://www.pwabuilder.com/imageGenerator
   - https://realfavicongenerator.net/
   - Or use ImageMagick/GraphicsMagick

3. **Place generated icons** in `/frontend/public/` directory with names:
   - icon-72x72.png
   - icon-96x96.png
   - icon-128x128.png
   - icon-144x144.png
   - icon-152x152.png
   - icon-192x192.png
   - icon-384x384.png
   - icon-512x512.png

### Using ImageMagick

```bash
# Install ImageMagick
sudo apt-get install imagemagick  # Ubuntu/Debian
# OR
brew install imagemagick  # macOS

# Generate all sizes from a 1024x1024 source image
convert source-icon.png -resize 72x72 public/icon-72x72.png
convert source-icon.png -resize 96x96 public/icon-96x96.png
convert source-icon.png -resize 128x128 public/icon-128x128.png
convert source-icon.png -resize 144x144 public/icon-144x144.png
convert source-icon.png -resize 152x152 public/icon-152x152.png
convert source-icon.png -resize 192x192 public/icon-192x192.png
convert source-icon.png -resize 384x384 public/icon-384x384.png
convert source-icon.png -resize 512x512 public/icon-512x512.png
```

## Service Worker

The service worker is automatically configured by Vite PWA plugin.

## Testing PWA

1. Build the production version:
   ```bash
   npm run build
   ```

2. Serve the built files:
   ```bash
   npm run preview
   ```

3. Open Chrome DevTools → Application → Manifest to verify PWA setup

4. Test "Add to Home Screen" functionality on mobile devices

## PWA Features Enabled

- ✅ Installable as app on mobile and desktop
- ✅ Offline functionality
- ✅ Service worker for caching
- ✅ App manifest configured
- ✅ App icons ready (need to be generated)
- ✅ Theme color and splash screen

## Deployment Checklist

- [ ] Generate all required icon sizes
- [ ] Update theme_color in manifest.json if needed
- [ ] Test PWA on real devices
- [ ] Verify offline functionality
- [ ] Test "Add to Home Screen" on iOS and Android
- [ ] Check PWA score in Lighthouse
