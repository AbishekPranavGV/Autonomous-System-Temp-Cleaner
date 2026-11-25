# Part 1 of the generator script
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent

# Define the HTML template strings
HEAD_HTML = '''<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NUNES AI PC Command Center — Version 10.0 | Enterprise Windows Diagnostics & Fleet Sentry</title>
  <meta name="description" content="Production-grade Windows optimization, deterministic diagnostics, zero-loss cleanup, and secure fleet management for NUNES Instruments office computers.">

  <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#f0f7ff',
              100: '#e0f2fe',
              200: '#bae6fd',
              300: '#7dd3fc',
              400: '#38bdf8',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
              800: '#075985',
              900: '#0c4a6e',
            }
          }
        }
      }
    };
  </script>

  <style>
    /* Professional Light-Blue & Crisp White Theme */
    html.light body {
      background-color: #f0f7ff;
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(2, 132, 199, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 90% 90%, rgba(14, 165, 233, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(224, 242, 254, 0.35) 0%, transparent 60%);
      color: #0f172a;
    }

    html.light .app-window, html.light .surface-card {
      background: #ffffff;
      border: 1px solid #e0f2fe;
      box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.07), 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    html.light .primary-btn {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
    }

    html.light .subtle-pill {
      background: #f0f7ff;
      border: 1px solid #bae6fd;
      color: #0369a1;
    }

    /* Dark Theme */
    html.dark body {
      background-color: #0b1329;
      background-image: 
        radial-gradient(circle at 50% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(2, 132, 199, 0.05) 0%, transparent 50%);
      color: #f8fafc;
    }

    html.dark .app-window, html.dark .surface-card {
      background: #111d38;
      border: 1px solid rgba(56, 189, 248, 0.15);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }

    html.dark .primary-btn {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
    }

    html.dark .subtle-pill {
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #38bdf8;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(100, 116, 139, 0.3); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(100, 116, 139, 0.5); }

    /* Tab navigation buttons */
    .nav-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.375rem;
      padding: 0.45rem 0.85rem;
      border-radius: 0.75rem;
      font-size: 0.75rem;
      font-weight: 700;
      white-space: nowrap;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      color: #64748b;
    }
    html.dark .nav-tab-btn { color: #94a3b8; }

    .nav-tab-btn:hover {
      color: #0284c7;
      background: rgba(2, 132, 199, 0.08);
    }
    html.dark .nav-tab-btn:hover {
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
    }

    .nav-tab-btn.active {
      color: #ffffff !important;
      background: #0284c7 !important;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }

    .section-view {
      display: none;
      animation: fadeIn 0.25s ease-out forwards;
    }
    .section-view.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>

<body class="min-h-screen py-3 px-2 sm:px-4 text-slate-800 dark:text-slate-100 font-sans antialiased">
'''
print("Loaded Part 1")
