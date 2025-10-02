<style>
    .widget-content-area {
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }

    body.dark .widget-content-area {
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
   }
   
   ul li {
     list-style-type: none;
   }

    :root {
      --bg: #0f172a;
      --bg-card: #1e293b;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #6366f1;
      --accent-hover: #818cf8;
      --success: #10b981;
      --border: #334155;
      --radius: 12px;
      --shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
      --transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    header {
      padding: 0 0 30px;
    }

    header h1 {
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(90deg, #818cf8, #6366f1, #3b82f6);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      margin-bottom: 12px;
    }

    header p {
      font-size: 1.1rem;
      color: var(--text-muted);
      margin: 0 auto;
    }

    .tabs {
      display: flex;
      gap: 2px;
      background: var(--border);
      border-radius: var(--radius);
      width: fit-content;
      overflow: hidden;
    }

    .tab {
      padding: 12px 24px;
      background: var(--bg-card);
      color: var(--text-muted);
      border: none;
      cursor: pointer;
      font-weight: 600;
      transition: var(--transition);
    }

    .tab.active {
      background: var(--accent);
      color: white;
    }

    .params {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 16px;
      margin: 16px 0;
    }

    .param {
      background: rgba(99, 102, 241, 0.08);
      padding: 16px;
      border-radius: 8px;
    }

    .param .name {
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 6px;
    }

    .param .badge {
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: bold;
    }

    .badge-required { background: #ef4444; color: white; }
    .badge-optional { background: #f59e0b; color: #000; }

    .example-box {
      background: #0f172a;
      border-left: 3px solid var(--accent);
      padding: 18px;
      border-radius: 8px;
      margin: 16px 0;
      position: relative;
    }

    .example-box code {
      color: #60a5fa;
      font-family: 'SFMono-Regular', Consolas, monospace;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .copy-btn {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(255,255,255,0.1);
      border: none;
      color: var(--text-muted);
      width: 32px;
      height: 32px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .copy-btn:hover {
      background: rgba(255,255,255,0.2);
      color: white;
    }

    .try-it {
      display: flex;
      gap: 12px;
      margin: 16px 0;
      flex-wrap: wrap;
    }

    .try-it input, .try-it select, .try-it button {
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0f172a;
      color: white;
      font-size: 0.95rem;
    }

    .try-it button {
      background: var(--accent);
      color: white;
      border: none;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }

    .try-it button:hover {
      background: var(--accent-hover);
    }

    .response {
      margin-top: 20px;
      max-height: 400px;
      overflow: auto;
      background: #0c111d;
      padding: 16px;
      border-radius: 8px;
      font-family: monospace;
      white-space: pre;
      color: #a0aec0;
    }

    .tables-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }

    .table-card {
      background: var(--bg-card);
      border-radius: var(--radius);
      padding: 20px;
      transition: var(--transition);
      border: 1px solid var(--border);
    }

    .table-card:hover {
      border-color: var(--accent);
      transform: translateY(-4px);
    }

    .table-card h4 {
      font-size: 1.1rem;
      margin-bottom: 12px;
      color: #cbd5e1;
    }

    .table-card .desc {
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-bottom: 16px;
    }

    .table-card .actions a {
      display: inline-block;
      margin-right: 12px;
      color: var(--accent);
      text-decoration: none;
      font-size: 0.9rem;
    }

    .table-card .actions a:hover {
      text-decoration: underline;
    }
</style>
<link rel="stylesheet" type="text/css" href="<?=$xc['tmp_url'];?>/src/assets/css/light/apps/blog-post.css">
<link rel="stylesheet" type="text/css" href="<?=$xc['tmp_url'];?>/src/assets/css/dark/apps/blog-post.css">