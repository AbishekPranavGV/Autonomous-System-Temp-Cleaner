# -*- coding: utf-8 -*-
"""
Generates ultra-advanced SVG and multi-resolution PNG/ICO favicons for NUNES AI PC Command Center.
"""
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <!-- Background Outer Glow -->
    <filter id="outerGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="24" flood-color="#0284c7" flood-opacity="0.45"/>
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#38bdf8" flood-opacity="0.3"/>
    </filter>
    
    <!-- Core Lightning Bolt Glow -->
    <filter id="coreGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#38bdf8" flood-opacity="0.8"/>
      <feDropShadow dx="0" dy="2" stdDeviation="12" flood-color="#0284c7" flood-opacity="0.6"/>
    </filter>

    <!-- Deep Tech Squircle Gradient -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="40%" stop-color="#0b132b"/>
      <stop offset="100%" stop-color="#030712"/>
    </linearGradient>

    <!-- Border Ring Gradient -->
    <linearGradient id="borderGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="30%" stop-color="#0ea5e9"/>
      <stop offset="70%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>

    <!-- High-Voltage Monogram Gradient -->
    <linearGradient id="boltGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="25%" stop-color="#e0f2fe"/>
      <stop offset="60%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>

    <!-- Accent Energy Arc -->
    <linearGradient id="energyGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="50%" stop-color="#06b6d4"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>

    <!-- Specular Highlight Glass -->
    <linearGradient id="glassGloss" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <!-- Ambient Glow Layer -->
  <rect x="36" y="36" width="440" height="440" rx="112" fill="url(#bgGradient)" filter="url(#outerGlow)"/>

  <!-- Main Squircle Body -->
  <rect x="36" y="36" width="440" height="440" rx="112" fill="url(#bgGradient)"/>
  
  <!-- Sleek Cybernetic Border Ring (2.5D Rim) -->
  <rect x="38" y="38" width="436" height="436" rx="110" fill="none" stroke="url(#borderGradient)" stroke-width="12" stroke-opacity="0.95"/>

  <!-- Top Glass Sheen -->
  <path d="M 40 148 C 40 88, 88 40, 148 40 L 364 40 C 424 40, 472 88, 472 148 C 472 210, 360 260, 256 260 C 150 260, 40 210, 40 148 Z" fill="url(#glassGloss)"/>

  <!-- Quantum Mesh Radar Circles (Subtle Background Geometry) -->
  <circle cx="256" cy="256" r="160" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="8 12" stroke-opacity="0.35"/>
  <circle cx="256" cy="256" r="115" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 8" stroke-opacity="0.25"/>

  <!-- Central Emblem: Precision Stylized "N" with Integrated Lightning Volt Blade -->
  <g filter="url(#coreGlow)">
    <!-- Left Vertical Pillar of N -->
    <path d="M 124 138 C 124 122, 137 110, 153 110 L 175 110 C 191 110, 204 122, 204 138 L 204 374 C 204 390, 191 402, 175 402 L 153 402 C 137 402, 124 390, 124 374 Z" fill="url(#boltGradient)"/>

    <!-- Right Vertical Pillar of N -->
    <path d="M 308 138 C 308 122, 321 110, 337 110 L 359 110 C 375 110, 388 122, 388 138 L 388 374 C 388 390, 375 402, 359 402 L 337 402 C 321 402, 308 390, 308 374 Z" fill="url(#boltGradient)"/>

    <!-- Dynamic Diagonal Lightning Slash (N Core) -->
    <path d="M 188 116 L 332 322 L 298 322 L 324 396 L 180 190 L 214 190 Z" fill="url(#boltGradient)"/>
  </g>

  <!-- High-Energy Nexus Sparkle at Lightning Strike -->
  <circle cx="316" cy="356" r="12" fill="#ffffff" filter="url(#coreGlow)"/>
  <circle cx="316" cy="356" r="6" fill="#38bdf8"/>
  
  <!-- Autonomous Pulse Orbit Dot (Top-Right Live Status Indicator) -->
  <circle cx="410" cy="102" r="22" fill="#10b981" filter="url(#coreGlow)"/>
  <circle cx="410" cy="102" r="14" fill="#a7f3d0"/>
  <circle cx="410" cy="102" r="8" fill="#ffffff"/>
</svg>
"""

def create_raster_icon(size):
    """Draws a pixel-perfect high-contrast icon using Pillow for the target size."""
    # We render at 4x for smooth antialiasing, then downsample
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(canvas_size * 0.08)
    corner = int(canvas_size * 0.24)
    w = canvas_size - (pad * 2)

    # 1. Background Rounded Rectangle (Deep Obsidian Navy)
    # Draw gradient by vertical interpolation
    for y in range(pad, pad + w):
        t = (y - pad) / float(w)
        r = int(15 * (1 - t) + 3 * t)
        g = int(23 * (1 - t) + 7 * t)
        b = int(42 * (1 - t) + 18 * t)
        draw.line([(pad, y), (pad + w, y)], fill=(r, g, b, 255))

    # Mask to rounded rectangle
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([pad, pad, pad + w, pad + w], radius=corner, fill=255)
    
    # Composite background with mask
    bg = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    bg.paste(img, (0, 0), mask=mask)
    img = bg
    draw = ImageDraw.Draw(img)

    # 2. Glowing Border Ring
    border_width = max(scale * 2, int(canvas_size * 0.035))
    draw.rounded_rectangle([pad, pad, pad + w, pad + w], radius=corner, outline=(56, 189, 248, 240), width=border_width)

    # 3. Top Glass Highlight
    glass_h = int(w * 0.45)
    glass_mask = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    glass_draw = ImageDraw.Draw(glass_mask)
    for y in range(pad, pad + glass_h):
        alpha = int(55 * (1.0 - (y - pad) / float(glass_h)))
        glass_draw.line([(pad + border_width, y), (pad + w - border_width, y)], fill=(255, 255, 255, alpha))
    img.paste(glass_mask, (0, 0), mask=mask)
    draw = ImageDraw.Draw(img)

    # 4. Central "N" Monogram with Lightning Slash
    col_w = int(canvas_size * 0.15)
    stem_top = int(canvas_size * 0.22)
    stem_bot = int(canvas_size * 0.78)
    col_left = int(canvas_size * 0.25)
    col_right = int(canvas_size * 0.60)
    col_radius = int(col_w * 0.35)

    # Left pillar
    draw.rounded_rectangle([col_left, stem_top, col_left + col_w, stem_bot], radius=col_radius, fill=(224, 242, 254, 255))
    # Right pillar
    draw.rounded_rectangle([col_right, stem_top, col_right + col_w, stem_bot], radius=col_radius, fill=(56, 189, 248, 255))

    # Diagonal lightning bolt
    diag_pts = [
        (col_left + int(col_w * 0.8), stem_top + int(scale * 4)),
        (col_right + int(col_w * 0.6), stem_bot - int(canvas_size * 0.20)),
        (col_right, stem_bot - int(canvas_size * 0.20)),
        (col_right + int(col_w * 0.5), stem_bot),
        (col_left + int(col_w * 0.3), stem_top + int(canvas_size * 0.20)),
        (col_left + col_w, stem_top + int(canvas_size * 0.20))
    ]
    draw.polygon(diag_pts, fill=(255, 255, 255, 255))

    # 5. Live Pulse Indicator (Green Emerald Sentry Dot at Top-Right)
    dot_r = max(scale * 3, int(canvas_size * 0.075))
    dot_cx = pad + w - int(dot_r * 1.5)
    dot_cy = pad + int(dot_r * 1.5)
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=(16, 185, 129, 255), outline=(255, 255, 255, 240), width=max(1, scale))

    # Downsample using high-quality Lanczos resampling
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def generate_all():
    print("[*] Generating NUNES Enterprise Favicons & Browser Tab Icons...")
    
    # 1. Save SVG
    svg_path = Path("favicon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(SVG_CONTENT.strip())
    print(f" [OK] Created vector {svg_path} ({len(SVG_CONTENT)} bytes)")

    # 2. Generate PNGs
    sizes = [16, 32, 48, 64, 180, 192, 512]
    images = {}
    for s in sizes:
        img = create_raster_icon(s)
        images[s] = img
        if s == 16:
            img.save("favicon-16x16.png")
            print(" [OK] Created favicon-16x16.png")
        elif s == 32:
            img.save("favicon-32x32.png")
            print(" [OK] Created favicon-32x32.png")
        elif s == 180:
            img.save("apple-touch-icon.png")
            print(" [OK] Created apple-touch-icon.png (180x180)")
        elif s == 192:
            img.save("android-chrome-192x192.png")
            print(" [OK] Created android-chrome-192x192.png")
        elif s == 512:
            img.save("android-chrome-512x512.png")
            print(" [OK] Created android-chrome-512x512.png")

    # 3. Generate multi-resolution favicon.ico containing 16x16, 32x32, 48x48
    ico_img = images[48]
    ico_img.save(
        "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print(" [OK] Created multi-resolution favicon.ico (16px, 32px, 48px)")

    # 4. Generate site.webmanifest for PWA and Windows pinned tabs
    manifest = """{
  "name": "NUNES AI PC Command Center",
  "short_name": "NUNES Fleet",
  "description": "Autonomous Windows Optimization, Deterministic Win32 Diagnostics & Safe Fleet Management",
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/favicon.svg",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ],
  "theme_color": "#0284c7",
  "background_color": "#0b1120",
  "display": "standalone",
  "start_url": "/"
}"""
    with open("site.webmanifest", "w", encoding="utf-8") as f:
        f.write(manifest)
    print(" [OK] Created site.webmanifest")

if __name__ == '__main__':
    generate_all()
